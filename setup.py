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

version = '2.0a1'

distfiles = """
    README.md
    setup.py
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


setup(
    name='piksemel',
    version=version,
    author='TUBITAK/UEKAE, Safa Arıman, Erdem Ersoy, Ersoy Kardesler',
    description='Python XML API based on the iksemel library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    ext_modules=[
        Extension(
            'piksemel',
            sources=['src/iksemel.c', 'src/pyiks.c'],
            extra_compile_args=["-fvisibility=default"]
        )
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: C',
        'Topic :: Text Processing :: Markup :: XML',
    ],
)
