==================================
:mod:`zeiss_r5` -- Zeiss R5 format
==================================

.. moduleauthor:: Stefano Costa
.. versionadded:: 0.4

The R5 format is an evolution of the older R4 format and is similar to the
:py:mod:`zeiss_rec_500` REC 500 format. It can be used for both processed
Cartesian data (Northing, Easting, Elevation) or for raw polar measurements,
but currently we don't have any sample data for the raw variant.

In each line of the data file, fields are separated by the ``|`` character::

    For R5|Adr 0008|KR NTR1100|X       21.259 m   |Y       59.620 m   |Z       11.256 m   |

The first field is always ``For R5`` and it indicates the format. Then the
``Adr`` field is a sequential id of the line, but not necessarily a surveyed
point.

The third field is the most important, as it specifies different types of
records with the first two characters, like ``TR`` or ``KR``. Then a space
character separates the next 7 characters, that are actually two separate
pieces of information: the “text code” in the first 3 characters (that can be
used to identify various points from the same feature or structure) and the
point number in the next four characters.

The next fields are the X, Y and Z values.
