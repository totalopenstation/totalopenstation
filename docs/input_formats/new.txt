.. _if_new:

===========================
 Adding a new input format
===========================

There are hundreds of survey data formats out there. One by one, we
will get them added into Total Open Station. Here's a general process
that defines some minimum requirements when implementing new formats.

Documentation
=============

Always write documentation for the format. Add a new document in the
``docs/input_formats/`` directory of the source tree with a bare
description, including:

- raw (polar) or processed (cartesian) format
- fixed-position based or fluid -- this changes the way the parser
  should work
- which devices or manufacturers use this format
- name of contributors

Shortcomings of Total Open Station that the format exposes shouldn't
be hidden, but rather made explicit both in code and documentation.

Sample data
===========

Never commit support for a new format without including the relevant
sample data in the ``sample_data`` directory. Generally speaking,
sample data files should follow these simple rules:

- quality is better than quantity, so prefer a smaller file with many
  different corner cases rather than a larger file with a bulk of
  ordinary data
- multiple files are OK, if they serve the purpose of showing
  different issues with the format
- files should be named with the same name of the Python module that
  implements the format, using a ``.tops`` extension, like
  ``topcon_gts.tops`` for a format implemented in a module named
  ``topcon_gts.py`` -- this will allow for simple automated tests

Code
====

When you have fulfilled the two previous tasks, you can start writing
code (or at least you should pretend doing that). New code is always
better than old code, because you have learned better programming
techniques, or because you are more confident with Total Open
Station. Writing tests for your code isn't (yet) required, but it's
highly encouraged. Don't break current practice.

All code implementing new formats should not break the existing
API. Changing the API should be done at the scale of the entire
library, to take into account the many different needs of each format
and parser. The development of Total Open Station is not in a stable
shape, so expect the API to change in future versions. However, please
understand that a new format parser is not the right place to do that.

Experiments are welcome. Mercurial allows for easy branching: you are
encouraged to clone our repository and go crazy with new features,
formats.
