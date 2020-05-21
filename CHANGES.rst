*********
Changelog
*********

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
