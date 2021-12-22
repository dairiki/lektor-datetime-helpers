*********
Changelog
*********

Release 1.0.1 (2021-12-22)
==========================

Packaging
---------

- Set ``Requires-Python: >=3.6`` in METADATA
- Deleted ``setup.py``

Testing
-------

- Add work-around for lektor bug `#974`_
- Test under python 3.10, and lektor<3.3

.. _#974: https://github.com/lektor/lektor/pull/974

Release 1.0.0 (2021-08-16 — yanked)
===================================

This release drops support for Python 2 and Python 3.5.

This release has been yanked_ from PyPI due to missing
``Requires-Python`` in METADATA allowing (broken) installation under
py27.  Use release 1.0.1 instead.

.. _yanked: https://pypi.org/help/#yanked

Dependencies
------------

This package no longer has any external dependencies.  Since python
3.6, ``datetime.astimezone()`` has the ability to interpret a naïve
``datetime`` w.r.t. the system local timezone, so the use of
``tzlocal`` is no longer necessary.

Release 0.3.3.post1 (2021-08-16)
================================

- Fix useless comparison in test.
- Fix formatting in ``CHANGES.rst``.


Release 0.3.3 (2021-08-15)
==========================

Bugs
----

- Pin ``tzlocal<3``.  (``Tzlocal >= 3`` drops support for python 2.)

Release 0.3.2 (2020-11-19)
==========================

Bugs
----

- Ensure that ``comparable_date`` and ``comparable_datetime`` objects
  are hashable.  This fixes issues using these classes with ``pytz``
  under py3k.
  
Testing
-------

- Test under py3.9

Release 0.3.1 (2020-05-21)
==========================

This release freshens the packaging.
There are no substantive changes to the code in this release.

Packaging
---------

- Update packaging to :PEP:`517`.

- Update LICENSE to latest 3-clause BSD text.

Docstrings
----------

- Fix docstring syntax.  No substantive changes.

Tests
-----

- Test under python 3.7 and 3.8.

- Use ``twine check`` rather than ``setup.py check`` to test
  description syntax.

Release 0.3 (2018-01-18)
========================

Fix things so that date and datetime types returned by the ``dateordatetime`` Lektor type are comparable against ``None``.  (``None`` compares less than all other dates and datetimes.)


Release 0.2 (2017-08-04)
========================

New features
------------

Make lists of ``dateordatetime`` types sortable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``dateordatetime`` custom Lektor type now returns subclasses of ``datetime.date`` or ``datetime.datetime`` which can be compared against one another.  Normally, attempts to compare a ``date`` against a ``datetime`` results in a ``TypeError`` being raised.  This made it difficult to sort on ``dateordatetime`` values.

Now ``date``\s sort before any ``datetime``\s with the same date.  Naïve ``datetime``\s sort before timezone-aware ``datetime``\s with the same date.

Release 0.1 (2017-04-19)
========================

Initial release.
