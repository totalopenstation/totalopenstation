---
layout: post
title: "Total Open Station 0.5 release, based on Python 3"
date: 2019-11-25 18:10 CEST
---

Total Open Station 0.5 is here!

This release is the result of a short and intense development cycle.

The application is now based on **Python 3**, which means an improved handling of data transfers and a general improvement of the underlying source code.

An extensive **test suite** based on _[pytest](http://pytest.org/)_ was added to help developers work with more confidence and the documentation was reorganized to be more readable.

There are only minor changes for users but this release includes a **large number of bugfixes and improvements** in the processing of data formats like Leica GSI, Carlson RW5 and Nikon RAW.

The command line program `totalopenstation-cli-parser` has four new options:

- `--2d` will drop Z coordinates so the resulting output only contains X and Y coordinates
- `--raw` will include all available data in the CSV output for further processing
- `--log` and `--logtofile` allow the logging of application output for debugging

If you were using a previous version of the program you can:

- wait for your Linux distribution to upgrade
- install with `pip install --upgrade totalopenstation` if you know your way around the command line on Linux or MacOS
- [download the Windows portable app from the release page](https://github.com/steko/totalopenstation/releases/tag/v0.5.0): this release is the first to support the Windows portable app from the start - for the moment this release supports 64-bit operating systems but we are working to add a version for older 32-bit systems.

But there's more. This release marks a renewed development process and the full onboarding of @psolyca in the team. With the 0.6 release we are planning to move the repository from the personal "steko" account to an organization account and improve the contribution guidelines so that the future of Total Open Station is not dependent on a single person. Of course we have already great plans for new features, as always listed on our issue tracker.

If you use Total Open Station please let us know and maybe give us a star ★ on GitHub.
