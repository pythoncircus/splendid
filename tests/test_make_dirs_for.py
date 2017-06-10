# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
from tempfile import mkdtemp
from shutil import rmtree

from splendid import make_dirs_for


def test_make_dirs_for():
    # Some setup to get a dir where this test can write...
    tmpdir = mkdtemp()

    # Actual example:
    my_filepath = os.path.join(tmpdir, 'some', 'dirs', 'testfile.txt')
    with open(make_dirs_for(my_filepath), 'w') as f:
        f.write("hello world")

    # Cleanup:
    rmtree(tmpdir)
