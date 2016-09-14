.. _release:

============================================
 Releasing a new Total Open Station version
============================================

Translations
============

The main tool we use for translating Total Open Station is `Transifex`_.

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

Documentation
=============

The documentation is included in the source tree, and is published
online at <http://totalopenstation.readthedocs.org/>_.

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

A portable Windows app is built with PyInstaller:

1. follow the instructions for `installing PyInstaller on Windows`_ (be sure to
   install pip-Win and create a virtual environment)
2. in the virtual environment, cd into the root directory of the
   totalopenstation source code and ``pip install .`` to install the current
   version of totalopenstation and all the dependencies
3. run ``pyinstaller totalopenstation-gui.spec``
4. this will create the file ``dist/totalopenstation.exe``, a portable
   single-file executable that will run from any compatible Windows system,
   even from USB sticks
5. an executable built on 64 bit systems will not run on 32 bit systems

.. _`installing PyInstaller on Windows`: http://pyinstaller.readthedocs.io/en/stable/installation.html#installing-in-windows
