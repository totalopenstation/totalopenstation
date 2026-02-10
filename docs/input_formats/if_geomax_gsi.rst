.. _if_geomax_gsi:

===========================
:mod:`geomax_gsi` -- GSI
===========================

.. moduleauthor:: Enzo Cocca

.. versionadded:: 0.7

Geomax total stations export data in the GSI (GEO Serial Interface) format,
which is fully compatible with the Leica GSI format. This module provides
an alias to the Leica GSI parser for Geomax instruments.

For full details about the GSI format structure, data blocks, and word
indices, see :ref:`if_leica_gsi`.

Supported devices
=================

Geomax total stations that export in GSI format, including:

- Geomax Zoom series
- Geomax Zipp series

Sample data
===========

GSI8 format::

   110001+00000001 21.322+03496940 22.322+09364360 31..00+00030485 51..1.+0000+000 87..10+00001500 81..00+00515836 82..00+00525871 83..00+00003079

Data fields are identical to the Leica GSI format (see :ref:`if_leica_gsi`).

.. seealso::

   :ref:`if_leica_gsi`
      Full documentation of the GSI format.
