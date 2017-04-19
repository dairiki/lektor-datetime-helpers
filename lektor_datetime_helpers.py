# -*- coding: utf-8 -*-
"""Helpers for dealing with datetimes in lektor.

Currently this provides a ``dateordatetime`` model field type which can
contain either ``date``\s or ``datetime``\s.  Also the following jinja
filters are provided:

isoformat(dt)
   Returns an iso formatted version the datetime, with timezone information.
   If ``dt`` is naive, it is localized to the site's default timezone.

localize_datetime(dt)
   If ``dt`` is naive, it is localized to the site's default timezone.

"""
from jinja2 import Undefined
from lektor.pluginsystem import Plugin
from lektor.types import DateType, DateTimeType
from tzlocal import get_localzone


class DateOrDateTimeType(DateTimeType, DateType):
    """A Lektor type which accepts either a date or datetime.
    """
    def value_from_raw(self, raw):
        value = DateTimeType.value_from_raw(self, raw)
        if isinstance(value, Undefined):
            value = DateType.value_from_raw(self, raw)
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
