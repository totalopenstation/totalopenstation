---
layout: post
title: "Total Open Station: a specialised format converter"
date: 2017-01-03 12:03 CET
---


It's 2017 and
[nine years ago](http://steko.iosa.it/2008/02/cat-devtotal_station-file/)
I started writing a set of Python scripts that would become Total Open
Station, a humble GPL-licensed tool to download and process data from
total station devices. I started from scratch, using the Python
standard library and pySerial as best as I could, to create a small
but complete program. Under the hood, I've been “religiously”
following the UNIX philosophy of *one tool that does one thing well*
and that is embodied by the two command line programs that perform the
separate steps of:

1. downloading data via a serial connection
2. converting the raw data to formats that can be used in GIS or CAD
   environments 

And despite starting as an itch to scratch, I also wanted TOPS to be
used by others, to provide something that was absent from the free
software world at the time, and that is still unchallenged in that
respect. So a basic and ugly graphical interface was created,
too. That gives a more streamlined view of the work, and largely
increases the number of potential users. Furthermore, TOPS can run not
just on Debian, Ubuntu or Fedora, but also on macOS and Windows and it
is well known that users of the latter operating systems don't like
too much working from a terminal.

Development has always been slow. After 2011 I had only occasional use
for the software myself, no access to a real total station, so my
interest shifted towards giving a good architecture to the program and
extending the number of formats that can be imported and exported. In
the process, this entailed rewriting the internal data structures to
allow for more flexibility, such as differentiating between point,
line and polygon geometries.

Today, I still find GUI programming out of my league and interests. If
I'm going to continue developing TOPS it's for the satisfaction of
crafting a good piece of software, learning new techniques in Python
or maybe rewriting entirely in a different programming language. It's
clear that the core feature of TOPS is not being a workstation for
survey professionals (since it cannot compete with the existing market
of proprietary solutions that come attached to most devices), but
rather becoming a polyglot converter, capable of handling dozens of
raw data formats and flexibly exporting to good standard
formats. *Flexibly exporting* means that TOPS should have features to
filter data, to reproject data based on fixed base points with known
coordinates, to create separate output files or layers and so
on. Basically, to adapt to many more needs than it does now. From a
software perspective, there are a few notable examples that I've been
looking at for a long time: [Sphinx](http://www.sphinx-doc.org/),
[GPSBabel](https://www.gpsbabel.org/) and
[Pandoc](http://pandoc.org/).

Sphinx is a *documentation generator* written in Python, the same
language I used for TOPS. You write a light markup source, and Sphinx can
convert it to several formats like HTML, ePub, LaTeX (and PDF),
groff. You can write short manuals, like the one I wrote for TOPS, or
entire books. Sphinx accepts many options, mostly from a configuration
file, and I took a few lines of code that I liked for handling the
internal dictionary (key-value hash) of all input and output formats
with conditional import of the selected module (rather than importing
all modules that won't be used). Sphinx is clearly excellent at what
it does, even though the similarities with TOPS are not many. After
all, TOPS has to deal with many undocumented raw formats while Sphinx
has the advantage of only one standard format. Sphinx was originally
written by Georg Brandl, one of the best Python developers and a
contributor to the standard library, in a highly elegant
object-oriented architecture that I'm not able to replicate.

GPSBabel is a venerable and excellent program for *GPS data conversion
and transfer*. It handles dozens of formats in read/write mode and
each format has “suboptions” that are specific to it. GPSBabel has
also advanced filtering capabilities, it can merge multiple input
files and since a few years there is a minimal graphical
interface. Furthermore, GPSBabel is integrated in GIS programs like
QGIS and can work in a variety of ways thanks to its programmable
command line interface. A strong difference with TOPS is that many of
the GPS data formats are binary, and that the basic data structures of
waypoints, tracks and routes is essentially the same (contrast that
with the monster LandXML specification, or the dozens of possible
combinations in a Leica GSI file). GPSBabel is written in portable
C++, that I can barely read, so anything other than inspiration for
the user interface is out of question.

Pandoc is a *universal document converter* that reads many markup
document formats and can convert to a greater number of formats
including PDF (via LaTeX), docx, OpenDocument. The baseline format for
Pandoc is an enriched Markdown. There are two very interesting
features of Pandoc as a source of inspiration for a converter: the
internal data representation and the Haskell programming language. The
internal representation of the document in Pandoc is an *abstract
syntax tree* that is not necessarily as expressive as the source
format (think of all the typography and formatting in a printed
document) but it can be serialised to/from JSON and allows filters to
work regardless of the input or output format. Haskell is a functional
language that I have never programmed, although it lends to creating
complex and efficient programs that are easily extended. Pandoc works
from the command line and has a myriad of options -- it’s also rather
common to
[invoke it from Makefiles](https://github.com/kjhealy/pandoc-templates/blob/master/makefile/Makefile)
or short scripts since one tends to work iteratively on a document. I
could see a future version of TOPS being rewritten in Haskell.

Scriptability and mode of use seem both important concepts to keep in
mind for a data converter. For total stations, a common workflow is to
download raw data, archive the original files and then convert to
another format (or even insert directly into a spatial database). With
the two programs `totalopenstation-cli-connector` and
`totalopenstation-cli-parser` such tasks are easily automated in a
single master script (or batch procedure) using a timestamp as
identifier for the job and the archived files. This means that once
the right parameters for your needs are found, downloading, archiving
and loading survey data in your working environment is **a matter of
seconds**, with no point-and-click, no icons, no mistakes. Looking at
GPSBabel, I wonder whether keeping the two programs separate really
makes sense from a UX perspective, as it would be more intuitive to
have a single `totalopenstation` executable. In fact, this dual
approach is a direct consequence of the small footprint of
`totalopenstation-cli-connector`, that merely acts as a convenience
layer on top of pySerial.

It's also important to think about maintainability of code: I have
little interest in developing the perfect UI for TOPS, all the time
spent for development is removed from my spare time (since no one is
paying for TOPS) and it would be way more useful if dedicated plugins
existed for popular platforms (think QGIS, gvSIG, even ArcGIS supports
Python, not to mention CAD software). At this time TOPS supports ten
(yes, 10) input formats out of ... hundreds, I think (some of which
are
[proprietary, binary formats](https://github.com/steko/totalopenstation/issues/38)). Expanding
the list of supported formats is the single aim that I see as
reasonable and worth of being pursued.
