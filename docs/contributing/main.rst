.. _contributing:

===================================
 Contributing to Total Open Station
===================================

Total Open Station is free software, released under the GNU `General
Public License v3`_ or (at your option) any later version.

.. _`General Public License v3`: http://www.gnu.org/licenses/gpl-3.0.html

Development is tracked with git. The main development repository is at
`GitHub`_ where it's easy to fork the source code. |br|
Experiments are welcome. Git allows for easy branching: you are
encouraged to clone our repository and go crazy with new features,
formats.


Coding standards
================

We try to follow as much as possible `PEP-8 <http://www.python.org/dev/peps/pep-0008/>`_


Translations
============

Helping
-------

The main tool we use for translating Total Open Station is `Transifex`_.

We are happy to accept translations for Total Open Station. Translations can
be easily submitted and reviewed at our Transifex_ page.
Translators get recognition for their valuable work.

If your native language is missing, why don't you start translating
Total Open Station right now?

Releasing
---------

When the release is approaching and the source strings are not going
to change, declare string freeze. Source messages should be updated
with one of ``xgettext``, ``pygettext`` or Babel_ (with the
``extract_messages`` command), producing ``totalopenstation.pot``, e.g.::

    xgettext  scripts/*.py -o locale/totalopenstation.pot

The resulting PO template file mut be uploaded to Transifex for translators
to work with::

    tx push -s

If there is an existing translation, ``msgmerge`` or Babel
``update_catalog`` should be used to update.

Translators should be invited to submit new translations, either via
``.po`` files or Transifex_.

When the translation period is over, pull the updated ``.po`` files
from Transifex with::

    tx pull -r totalopenstation.totalopenstation-app -a

and check that the files are updated. Commit new files separately from updates.

.. _Babel: http://babel.edgewall.org/wiki/Documentation/0.9/setup.html
.. _Transifex: https://www.transifex.com/projects/p/totalopenstation/resource/totalopenstation-app/

If using Babel, compile the translated messages with::

    python setup.py compile_catalog -d locale


=======================================
 Using Total Open Station as a library
=======================================

All the functionality implemented in Total Open Station can be used
independently, with the exception of the user interfaces.

In other words, the classes for reading specific formats and those for writing
well-known formats are entirely usable on their own.

This is a feature.

Example: a web app for converting total station data
====================================================

If you want to see how to write a web app to convert total station
data in 50 lines of Python code, check out `TOPS in the Cloud
<https://bitbucket.org/steko/tops-cloud/overview>`_. It is made with
`Flask <http://flask.pocoo.org/>`_ and shows how to use Total Open
Station as a programming library.

.. warning::
    TOPS in the Cloud is not maintained and does not receive security
    updates. Please don't use it in production.

==================================
Developing with Total Open Station
==================================

General remarks
===============

.. _new:

Adding a new format
-------------------

There are hundreds of survey data formats out there. One by one, we
will get them added into Total Open Station. Here's a general process
that defines some minimum requirements when implementing new formats
as input or output.

Documentation
_____________

Always write documentation for the format. Add a new document in the
``docs/input_formats/`` directory or amend the
``docs/output_formats/of_implemented.rst`` file of the source tree with a bare
description, including:

- raw (polar) or processed (cartesian) format
- fixed-position based or fluid -- this changes the way the parser
  should work (input format)
- which devices, manufacturers or software use this format
- name of contributors
- reference to the format if available

Shortcomings of Total Open Station that the format exposes shouldn't
be hidden, but rather made explicit both in code and documentation.

Sample data
___________

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
____

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

Processing data
===============

Total Open Station use GeoJSON as its internal processing data following the
`RFC 7946 <https://tools.ietf.org/html/rfc7946>`_ standard. |br|
The library used to handle this format is
`PyGeoif <https://github.com/cleder/pygeoif/>`_. |br|

Thus, all data are build around a :class:`formats.Feature` class. |br|
To be able to evaluate which type of data a :class:`formats.Feature` holds,
a descriptor has been added as a property. |br|
Those descriptors are:

+------------+---------------------------------+-------------------------------------------+
| Descriptor |           Explanation           |        Construction                       |
+============+=================================+===========================================+
| PT         | Simple point                    | .. code:: python                          |
|            |    only coordinates             |                                           |
|            |                                 |    Feature(point,                         |
|            |                                 |            desc='PT',                     |
|            |                                 |            id=pid,                        |
|            |                                 |            point_name=point_name,         |
|            |                                 |            dist_unit=dist_unit,           |
|            |                                 |            attrib=attrib)                 |
+------------+---------------------------------+-------------------------------------------+
| PO         | Complexe point                  | .. code:: python                          |
|            |   all information needed to     |                                           |
|            |   compute coordinates           |    Feature(point,                         |
|            |                                 |            desc='PO',                     |
|            |                                 |            id=pid,                        |
|            |                                 |            point_name=point_name,         |
|            |                                 |            angle_unit=angle_unit,         |
|            |                                 |            z_angle_type=z_angle_type,     |
|            |                                 |            dist_unit=dist_unit,           |
|            |                                 |            dist_type=dist_type,           |
|            |                                 |            azimuth=azimuth,               |
|            |                                 |            angle=angle,                   |
|            |                                 |            z_angle=z_angle,               |
|            |                                 |            dist=dist,                     |
|            |                                 |            th=th,                         |
|            |                                 |            ih=ih,                         |
|            |                                 |            ppm=ppl,                       |
|            |                                 |            prism_constant=prism_constant, |
|            |                                 |            station_name=station_name,     |
|            |                                 |            attrib=attrib)                 |
+------------+---------------------------------+-------------------------------------------+
| ST         | Station point data              | .. code:: python                          |
|            |                                 |                                           |
|            |                                 |    Feature(point,                         |
|            |                                 |            desc='ST',                     |
|            |                                 |            id=pid,                        |
|            |                                 |            point_name=station_name,       |
|            |                                 |            angle_unit=angle_unit,         |
|            |                                 |            dist_unit=dist_unit,           |
|            |                                 |            ih=ih,                         |
|            |                                 |            hz0=hz0,                       |
|            |                                 |            attrib=attrib)                 |
+------------+---------------------------------+-------------------------------------------+
| BS         | Backsight information           | .. code:: python                          |
|            |                                 |                                           |
|            |                                 |    Feature(point,                         |
|            |                                 |            desc='BS',                     |
|            |                                 |            id=pid,                        |
|            |                                 |            point_name=point_name,         |
|            |                                 |            angle_unit=angle_unit,         |
|            |                                 |            circle=circle)                 |
+------------+---------------------------------+-------------------------------------------+

Types of values passed to the :class:`formats.Feature` class are :

.. code-block:: python

    Feature(Point class,
            desc=str,
            id=int,
            point_name=str,
            angle_unit=str,
            z_angle_type=str,
            dist_unit=str,
            dist_type=str,
            angle=float,
            z_angle=float,
            dist=float,
            th=float,
            ih=float,
            hz0=float,
            circle=float,
            ppm=float,
            prism_constant=float,
            station_name=str,
            attrib=list)

Those values are properties of the :class:`formats.Feature` class.

Modules
=======

For more in-depth knowledge of classes, we encourage reading the code @ `Github`_.


.. toctree::
    :maxdepth: 1
    :glob:

    modules/*

============================================
 Releasing a new Total Open Station version
============================================

Documentation
=============

The documentation is included in the source tree, and is published
online at `http://totalopenstation.readthedocs.org/ <http://totalopenstation.readthedocs.org/>`_.

Manual pages for the three scripts provided with TOPS are not
available at the moment.

Release
=======

The version number is declared in ``totalopenstation/__init__.py`` and
is propagated in other places from there, including ``setup.py`` and
the “About” dialog.

A *source distribution* is made using::

  python setup.py sdist

A *built distribution* is made using (e.g. for Windows installer)::

  python setup.py bdist --formats wininst

We are currently following the `Python Packaging User Guide
<https://packaging.python.org/en/latest/distributing.html>`_ and
distributing sources and *wheels*.

Windows portable app
====================

A portable Windows app is built with PyInstaller. From the root
directory of the source repository of Total Open Station:

```
python.exe -m venv pyinst-env
source pyinst-env/Scripts/activate
pip.exe install -e .
pip.exe install PyInstaller
pyinstaller.exe totalopenstation-gui.spec
```

This will create the file ``dist/totalopenstation.exe``, a portable
single-file executable that will run from any compatible Windows system,
even from USB sticks

.. warning::

    An executable built on 64 bit systems will not run on 32 bit systems

.. _`installing PyInstaller on Windows`: http://pyinstaller.readthedocs.io/en/stable/installation.html#installing-in-windows
