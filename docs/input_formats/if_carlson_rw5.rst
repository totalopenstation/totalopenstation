=================================================================
 :mod:`carlson_rw5` -- Carlson SurvCE Raw Data File Format (RW5)
=================================================================

.. module:: carlson_rw5
    :platform: any
    :synopsis: Read data in the Carlson RW5 data format
.. moduleauthor:: Stefano Costa, Filip Kłosowski
.. versionadded:: 0.4

Carlson RW5 is an exchange format used by the Carlson SurvCE software.

The official documentation about the format is provided on the
`Carlson website`_.

.. _Carlson website: http://update.carlsonsw.com/kbase_attach/372/

RW5 is a rich format for raw data about the entire field operation of
total stations and even GPS. At the moment, a minimal subset of the
specification is supported, consisting of the ``OC``, ``BP``, ``LS``
and ``SS`` record types.

Each record is made of one line of text, with comma-separated fields::

  OC,OP111,N 16556174.237,E 942130.662,EL 16.404
  BK,OP111,BP108,BS0.00000,BC0.00000
  LS,HI5.684,HR5.500
  SS,OP111,FP108,AR0.00000,ZE0.00017,SD3.3566,--FENCE1

The first field is a two-letter code of the type of record. All the
following fields are composed with 1- or 2- letter field codes (such
as ``OP``, ``N `` or ``FP``) and numeric values. The “Notes” field is
introduced by the ``--`` code and contains a description of the
record.

*Sideshot* records (``SS``) reference the *Occupy point* record in the
``OP`` field. In practice, each point has a unique number and can be
referenced for various purposes from other records.

TOPS is capable of converting raw measurement data into local
coordinates, by performing a sequential processing of all records in
their order.
