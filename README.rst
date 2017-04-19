=================================================
Helpers for Dealing with ``datetime``\s in Lektor
=================================================

This is a plugin for Lektor which provides some helpers for dealing with
dates and times.

Currently this provides a ``dateordatetime`` model field type which
can contain either a ``date`` or a ``datetime``.

Also the following jinja filters are provided:

isoformat(dt)
   Returns an iso formatted version the datetime, with timezone information.
   If ``dt`` is naive, it is localized to the site's default timezone.

localize_datetime(dt)
   If ``dt`` is naive, it is localized to the site's default timezone.
