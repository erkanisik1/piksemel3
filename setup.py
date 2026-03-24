#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 TUBITAK/UEKAE, 2019 Safa Arıman, 2020 Erdem Ersoy
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys
import os
import glob
import shutil
import subprocess
from setuptools import setup, Extension

version = '3.0.0'

distfiles = """
    README.md
    setup.py
    pyproject.toml
    src/iksemel.c
    src/iksemel.h
    src/pyiks.c
    tests/*.py
"""

if 'sdist' in sys.argv:
    distdir = "piksemel-%s" % version
    filelist = []
    for t in distfiles.split():
        filelist.extend(glob.glob(t))
    if os.path.exists(distdir):
        shutil.rmtree(distdir)
    os.mkdir(distdir)
    for file_ in filelist:
        cum = distdir[:]
        for d in os.path.dirname(file_).split('/'):
            dn = os.path.join(cum, d)
            cum = dn[:]
            if not os.path.exists(dn):
                os.mkdir(dn)
        shutil.copy(file_, os.path.join(distdir, file_))
    subprocess.run(["tar", "czf", "piksemel-" + version + ".tar.gz", distdir])
    shutil.rmtree(distdir)
    sys.exit(0)

elif 'test' in sys.argv:
    fail = 0
    for test in os.listdir("tests"):
        if test.endswith(".py"):
            if 0 != subprocess.call(["tests/" + test]):
                fail += 1
                print(test, "failed!")
    if not fail:
        print("all tests passed :)")
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    # Modern setup with pyproject.toml compatibility
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        print("Use 'pip install .' instead of 'python setup.py install' for modern installation")
        sys.exit(1)
    
    setup(
        ext_modules=[
            Extension(
                'piksemel',
                sources=['src/iksemel.c', 'src/pyiks.c'],
                extra_compile_args=["-fvisibility=hidden"]
            )
        ],
    )
