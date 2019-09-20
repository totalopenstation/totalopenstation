==============================
Developping |tops|
==============================

.. _dev_advices:

Advices
=======

.. _new:

Adding a new format
-------------------

There are hundreds of survey data formats out there. One by one, we
will get them added into |tops|. Here's a general process
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

Shortcomings of |tops| that the format exposes shouldn't
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
and parser. The development of |tops| is not in a stable
shape, so expect the API to change in future versions. However, please
understand that a new format parser is not the right place to do that.

.. _dev_processing_data:

Processing data
===============

|tops| use GeoJSON as its internal processing data following the
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


.. _dev_modules:

Modules
=======

For more in-depth knowledge of classes, we encourage reading the code @ `Github`_.


.. toctree::
    :maxdepth: 1
    :glob:

    input_formats
    output_formats
    models
    test


