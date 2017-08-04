*********
Changelog
*********

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
