# Contribution Guidelines

## Table of Contents

- [Contribution Guidelines](#contribution-guidelines)
  - [Introduction](#introduction)
  - [Bug reports](#bug-reports)
  - [Discuss your design](#discuss-your-design)
  - [Testing](#testing)
  - [Translation](#translation)
  - [Code review](#code-review)
  - [Styleguide](#styleguide)
  - [Design guideline](#design-guideline)
  - [Developer Certificate of Origin (DCO)](#developer-certificate-of-origin-dco)
  - [Release Cycle](#release-cycle)
  - [Maintainers](#maintainers)
  - [Owners](#owners)
  - [Versions](#versions)
  - [Releasing Total Open Station](#releasing-total-open-station)
  - [Copyright](#copyright)

## Introduction

This document explains how to contribute changes to the Total Open Station project.
It assumes you have followed the
[installation instructions](https://totalopenstation.readthedocs.io/en/stable/installing.html),
with particular reference to the section detailing the use of pip and virtualenv.

## Bug reports

Please search the issues on the issue tracker with a variety of keywords
to ensure your bug is not already reported.

If unique, [open an issue](https://github.com/steko/totalopenstation/issues/new)
and answer the questions so we can understand and reproduce the
problematic behavior.

To show us that the issue you are having is in Total Open Station itself, please
write clear, concise instructions so we can reproduce the behavior—
even if it seems obvious. The more detailed and specific you are,
the faster we can fix the issue. Check out [How to Report Bugs
Effectively](http://www.chiark.greenend.org.uk/~sgtatham/bugs.html).

Please be kind, remember that Total Open Station comes at no cost to you, and you're
getting free help.

## Discuss your design

The project welcomes submissions. If you want to change or add something,
please let everyone know what you're working on—[file an issue](https://github.com/steko/totalopenstation/issues/new)!
Significant changes must go through the change proposal process
before they can be accepted. To create a proposal, file an issue with
your proposed changes documented, and make sure to note in the title
of the issue that it is a proposal.

This process gives everyone a chance to validate the design, helps
prevent duplication of effort, and ensures that the idea fits inside
the goals for the project and tools. It also checks that the design is
sound before code is written; the code review tool is not the place for
high-level discussions.

## Testing

Before submitting a pull request, run all the tests for the whole tree
to make sure your changes don't cause regression elsewhere.

Here's how to run the test suite:

- Install pytest
- Run pytest from the root of the source tree

## Translation

We do all translation work inside [Transifex](https://www.transifex.com/projects/p/totalopenstation/resource/totalopenstation-app/). Once a translation has reached
100% it will be synced back into this repo and
included in the next released version.

## Building Total Open Station

To build a distribution:

- python setup.py sdist bdist_wheel

Distributions are uploaded to PyPI with twine.

## Code review

Changes to Total Open Station must be reviewed before they are accepted—no matter who
makes the change, even if they are an owner or a maintainer. We use GitHub's
pull request workflow to do that. The repository is setup to ensure every PR
is reviewed by at least 1 maintainer.

Please try to make your pull request easy to review for us. And, please read
the [How to get faster PR reviews](https://github.com/kubernetes/community/blob/261cb0fd089b64002c91e8eddceebf032462ccd6/contributors/guide/pull-requests.md#best-practices-for-faster-reviews) guide;
it has lots of useful tips for any project you may want to contribute.
Some of the key points:

* Make small pull requests. The smaller, the faster to review and the
  more likely it will be merged soon.
* Don't make changes unrelated to your PR. Maybe there are typos on
  some comments, maybe refactoring would be welcome on a function... but
  if that is not related to your PR, please make *another* PR for that.
* Split big pull requests into multiple small ones. An incremental change
  will be faster to review than a huge PR.

## Styleguide

Currently we don't enforce any particular style other than PEP-8.

However, consider using [black](https://black.readthedocs.io/en/stable/).

## Design guideline

To maintain understandable code it is important to have a good structure of the code. At a general level, the Total Open Station library code is divided into the following parts:

- **formats:** Parsers for importing data, each format has a separate module
- **models:** Default settings for some total station devices
- **output:** Builders for exporting data, each format has a separate module
- **tests:** Tests for parsers and builders
- **utils:** Small functions that are needed for both command line and graphical interfaces


## Developer Certificate of Origin (DCO)

We consider the act of contributing to the code by submitting a Pull
Request as the "Sign off" or agreement to the certifications and terms
of the DCO and GNU General Public License. No further action is required.
Additionally you could add a line at the end of your commit message.

```
Signed-off-by: Joe Smith <joe.smith@email.com>
```

If you set your `user.name` and `user.email` git configs, you can add the
line to the end of your commit automatically with `git commit -s`.

We assume in good faith that the information you provide is legally binding.


## Maintainers

To make sure every pull request is checked, it **MUST** be reviewed by at least
one maintainer (or owner) before it can get merged. A maintainer
should be a contributor of Total Open Station and contributed at least
4 accepted PRs. The owners or the team maintainers may invite the contributor. A maintainer
should spend some time on code reviews.

For security reasons, Maintainers should use 2FA for their accounts and
if possible provide gpg signed commits.
https://help.github.com/articles/securing-your-account-with-two-factor-authentication-2fa/
https://help.github.com/articles/signing-commits-with-gpg/

## Owners

Total Open Station is a pure community organization without any company support.
Currently, the owners are @steko and @psolyca. A process to elect owners may
be introduced in the future if the number of maintainers will grow.

For security reasons, owners or any account with write access (like a bot)
must use 2FA.
https://help.github.com/articles/securing-your-account-with-two-factor-authentication-2fa/


## Versions

Total Open Station has the `master` branch as a tip branch and there are no version branches.
When a release is ready, we will tag `v0.6.0` for binary download. If `v0.6.0` has bugs, we will accept
bugfixes and publish a `v0.6.1` tag, from the master branch.

We follow [PEP-440 compatible semantic versioning](https://www.python.org/dev/peps/pep-0440/#id50).

## Releasing Total Open Station

For the moment, see the corresponding section in the documentation, [Releasing a new Total Open Station version](https://totalopenstation.readthedocs.io/en/stable/contributing/main.html#releasing-a-new-total-open-station-version).

## Copyright

Code that you contribute should use the standard copyright header:

```
// Copyright 2019 The Total Open Station Authors. All rights reserved.
// Use of this source code is governed by a MIT-style
// license that can be found in the LICENSE file.
```

Files in the repository contain copyright from the year they are added
to the year they are last changed. If the copyright author is changed,
just paste the header below the old one.
