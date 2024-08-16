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
from __future__ import annotations

import datetime
import operator
from typing import Any
from typing import Callable
from typing import overload
from typing import TypeVar

from jinja2 import Undefined
from lektor.pluginsystem import Plugin
from lektor.types import DateType, DateTimeType, RawValue

try:
    from types import NotImplementedType
except ImportError:  # pragma: no cover
    NotImplementedType = Any  # type: ignore[misc, assignment]


_Date = TypeVar("_Date", bound=datetime.date)


def _key(dt: datetime.date | None) -> tuple[Any, ...]:
    # ``date``\s sort before naive ``datetime``\s of the same date,
    # which, in turn, sort before aware ``datetime``\s.
    if isinstance(dt, datetime.datetime):
        tz_key: tuple[Any, ...]
        if dt.tzinfo is None:
            tz_key = (0,)
        else:
            tz_key = 1, dt.utcoffset()
        return (dt.year, dt.month, dt.day,
                tz_key,
                dt.hour, dt.minute, dt.second, dt.microsecond)

    if isinstance(dt, datetime.date):
        return dt.year, dt.month, dt.day

    assert dt is None
    mindt = datetime.datetime.min
    return (mindt.year - 1,)


def _make_richcomp_method(
    opname: str
) -> Callable[["_comparable_mixin", Any], bool | NotImplementedType]:
    op = getattr(operator, opname)

    def f(self: Any, other: Any) -> bool | NotImplementedType:
        if other is not None and not isinstance(other, datetime.date):
            return NotImplemented
        return op(_key(self), _key(other))  # type: ignore[no-any-return]
    f.__name__ = opname
    return f


class _comparable_mixin(object):
    locals().update(
        {
            opname: _make_richcomp_method(opname)
            for opname in (
                "__lt__", "__le__", "__gt__", "__ge__", "__eq__", "__ne__"
            )
        }
    )

    def __hash__(self) -> int:
        return super().__hash__()


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


class DateOrDateTimeType(DateTimeType, DateType):  # type: ignore[misc]
    """A Lektor type which accepts either a date or datetime.
    """
    def value_from_raw(
        self, raw: RawValue
    ) -> comparable_date | comparable_datetime | Undefined:
        value = DateTimeType.value_from_raw(self, raw)
        if isinstance(value, datetime.datetime):
            return comparable_datetime(value.year, value.month, value.day,
                                       value.hour, value.minute, value.second,
                                       value.microsecond, value.tzinfo,
                                       fold=value.fold)

        value = DateType.value_from_raw(self, raw)
        if isinstance(value, datetime.date):
            return comparable_date(value.year, value.month, value.day)

        assert isinstance(value, Undefined)
        return value


class DatetimeHelpersPlugin(Plugin):  # type: ignore[misc]
    name = u'datetime-helpers'
    description = __doc__

    @overload
    def localize_datetime(self, dt: _Date) -> _Date: ...

    @overload
    def localize_datetime(self, dt: None) -> None: ...

    def localize_datetime(
        self, dt: datetime.date | None
    ) -> datetime.date | None:
        if isinstance(dt, datetime.datetime) and dt.tzinfo is None:
            dt = dt.astimezone()
        return dt

    def isoformat(self, dt: datetime.date) -> str:
        return self.localize_datetime(dt).isoformat()

    def on_setup_env(self, **extra: Any) -> None:
        self.env.jinja_env.filters.update({
            'localize_datetime': self.localize_datetime,
            'isoformat': self.isoformat,
            })
        self.env.add_type(DateOrDateTimeType)
