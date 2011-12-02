# -*- coding: utf-8 -*-

# Copyright 2007-2011 by the Sphinx team http://sphinx.pocoo.org/

from os import path

__version__  = '0.3pre'

package_dir = path.abspath(path.dirname(__file__))

if '+' in __version__ or 'pre' in __version__:
    # try to find out the changeset hash if checked out from hg, and append
    # it to __version__ (since we use this value from setup.py, it gets
    # automatically propagated to an installed copy as well)
    try:
        import subprocess
        p = subprocess.Popen(['hg', 'id', '-i', '-R',
                              path.join(package_dir, '..')],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            __version__ += '/' + out.strip()
            print(__version__)
    except Exception:
        pass
