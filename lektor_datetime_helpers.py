# -*- coding: utf-8 -*-
"""Helpers for dealing with datetimes in lektor.

Currently this provides a ``dateordatetime`` model field type which can
contain either ``date``\\s or ``datetime``\\s.  Also the following jinja
filters are provided:

isoformat(dt)
   Returns an iso formatted version the datetime, with timezone information.
   If ``dt`` is naive, it is localized to the site's default timezone.

localize_datetime(dt)
   If ``dt`` is naive, it is localized to the site's default timezone.

"""
import datetime

from jinja2 import Undefined
from lektor.pluginsystem import Plugin
from lektor.types import DateType, DateTimeType
from tzlocal import get_localzone


def _key(dt):
    # ``date``\s sort before naive ``datetime``\s of the same date,
    # which, in turn, sort before aware ``datetime``\s.
    if isinstance(dt, datetime.datetime):
        if dt.tzinfo is None:
            tz_key = (0,)
        else:
            tz_key = 1, dt.utcoffset()
        return (dt.year, dt.month, dt.day,
                tz_key,
                dt.hour, dt.minute, dt.second, dt.microsecond)
    elif isinstance(dt, datetime.date):
        return dt.year, dt.month, dt.day
    elif dt is None:
        mindt = datetime.datetime.min
        return (mindt.year - 1,)
    else:
        raise TypeError("can't compare %s" % type(dt).__name__)


class _comparable_mixin(object):
    def make_cmp_(op):
        def f(self, other):
            left = _key(self)
            right = _key(other)
            return getattr(left, op)(right)
        f.__name__ = op
        return f

    for op_ in '__lt__', '__le__', '__gt__', '__ge__', '__eq__', '__ne__':
        locals()[op_] = make_cmp_(op_)

    del make_cmp_, op_


class comparable_date(_comparable_mixin, datetime.date):
    """ A ``date`` which is directly comparable to a ``datetime``.

    ``Date``\\s sort before all ``datetime``\\s with the same or a later
    date, and after all ``datetime``\\s with an earlier date.

    """


class comparable_datetime(_comparable_mixin, datetime.datetime):
    """A ``datetime`` which is directly comparable to a ``date``.

    ``Date``\\s sort before all ``datetime``\\s with the same or a later
    date, and after all ``datetime``\\s with an earlier date.

    Naive ``datetime``\\s sort before timezone-aware ``datetime``\\s of
    the same (or a later) date.

    """


class DateOrDateTimeType(DateTimeType, DateType):
    """A Lektor type which accepts either a date or datetime.
    """
    def value_from_raw(self, raw):
        value = DateTimeType.value_from_raw(self, raw)
        if not isinstance(value, Undefined):
            value = comparable_datetime(value.year, value.month, value.day,
                                        value.hour, value.minute, value.second,
                                        value.microsecond, value.tzinfo)
        else:
            value = DateType.value_from_raw(self, raw)
            if not isinstance(value, Undefined):
                value = comparable_date(value.year, value.month, value.day)
        return value


class DatetimeHelpersPlugin(Plugin):
    name = u'datetime-helpers'
    description = __doc__

    def localize_datetime(self, dt):
        if hasattr(dt, 'hour') and not dt.tzinfo:
            dt = self.default_timezone.localize(dt)
        return dt

    def isoformat(self, dt):
        return self.localize_datetime(dt).isoformat()

    def on_setup_env(self, **extra):
        self.default_timezone = get_localzone()

        self.env.jinja_env.filters.update({
            'localize_datetime': self.localize_datetime,
            'isoformat': self.isoformat,
            })
        self.env.add_type(DateOrDateTimeType)
