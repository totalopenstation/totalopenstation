---
layout: post
title: "Total Open Station 0.4 new release"
date: 2019-08-22 18:10 CEST
---

After two years of slow development, I took the opportunity of some days off to
finally release version 0.4, that was already available in beta since 2017.

No open bugs were left and this release is mature enough to hit the repositories.

Find it on PyPI at <https://pypi.python.org/pypi/totalopenstation> as usual.

Windows users, please note that the TOPS-on-a-USB-stick version will have to
wait a few days more, but the [beta version](https://tops.iosa.it/2016/06/22/portable-tops-beta.html) is equally functional.

### What's new in Total Open Station 0.4

The new version brings read support for 4 new formats:

- Carlson RW5 
- Leica GSI
- Sokkia SDR33
- Zeiss R5

Other input formats were improved, most notably Nikon RAW.

DXF output was improved, even though the default template is not very
useful since it is based on an old need from the time when TOPS was
developed day to day on archaeological excavations.

The work behind these new formats is in part by the new contributor to the
project, Damien Gaignon (find him as @psolyca on GitHub), who submitted a lot
of other code and started helping with project maintenance as well. I am
very happy to have Damien onboard and since my usage of TOPS is almost at zero,
it's very likely that I will hand over the development in the near future.

The internal data structures for handling the conversion between input and
output formats are completely new, and based on the Python GeoInterface
abstraction offered by the [`pygeoif`](https://pypi.org/project/pygeoif/)
library. This allows going beyond single points to managing lines and polygons,
even though no such feature is available at the moment. If you often record
linear or polygonal features that you're manually joining in the post-processing
stage, think about helping TOPS development and you could get DXF or Shapefiles
with the geometries ready to use (yes, Shapefile output is on our plans, too).

There were many bugfixes, more than 100 commits, 64 by Damien Gaignon and 52 by
myself (to be honest, many of my own commits are just merges!).

This version is the last built on Python 2, and work is already ongoing towards
a new version that will be based on Python 3: a more mature codebase will
mean a better program, without any visible drastic change.

