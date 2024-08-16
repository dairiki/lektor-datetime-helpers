#################################################
Helpers for Dealing with ``datetime``\s in Lektor
#################################################

.. image:: https://img.shields.io/pypi/v/lektor-datetime-helpers.svg
   :target: https://pypi.org/project/lektor-datetime-helpers/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/lektor-datetime-helpers.svg
   :target: https://pypi.python.org/pypi/lektor-datetime-helpers/
   :alt: PyPI Supported Python Versions

.. image:: https://img.shields.io/github/license/dairiki/lektor-datetime-helpers
   :target: https://github.com/dairiki/lektor-datetime-helpers/blob/master/LICENSE
   :alt: GitHub license

.. image:: https://github.com/dairiki/lektor-datetime-helpers/workflows/Tests/badge.svg
   :target: https://github.com/dairiki/lektor-datetime-helpers
   :alt: GitHub Actions (Tests)

************
Introduction
************

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
