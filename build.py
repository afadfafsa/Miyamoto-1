#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Miyamoto! Level Editor - New Super Mario Bros. U Level Editor
# Copyright (C) 2009-2019 Treeki, Tempus, angelsl, JasonP27, Kinnay,
# MalStar1000, RoadrunnerWMC, MrRean, Grop, AboodXD, Gota7, John10v10

# This file is part of Miyamoto!.

# Miyamoto! is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Miyamoto! is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Miyamoto!.  If not, see <http://www.gnu.org/licenses/>.

# build.py
# Builds Miyamoto! to a binary
# Use the values below to configure the release:

from globals import MiyamotoVersion

PackageName = 'miyamoto_v%s' % MiyamotoVersion
Version = MiyamotoVersion


################################################################
################################################################

# Imports
import os, os.path, platform, shutil, sys, zipfile
from cx_Freeze import setup, Executable
from shutil import copyfile

# Pick a build directory
dir_ = 'distrib/' + PackageName

# Print some stuff
print('[[ Freezing Miyamoto! ]]')
print('>> Destination directory: %s' % dir_)

# Add the "build" parameter to the system argument list
if 'build' not in sys.argv:
    sys.argv.append('build')

# Clear the directory
if os.path.isdir(dir_): shutil.rmtree(dir_)
os.makedirs(dir_)

# exclude QtWebKit to save space, plus Python stuff we don't use
excludes = ['doctest', 'pdb', 'unittest', 'difflib', 'inspect',
    'os2emxpath', 'posixpath', 'optpath', 'locale', 'calendar',
    'select', 'multiprocessing', 'ssl',
    'PyQt5.QtWebKit', 'PyQt5.QtNetwork']

# Set it up
base = 'Win32GUI' if sys.platform == 'win32' else None
setup(
    name = 'Miyamoto!',
    version = Version,
    description = 'Miyamoto!',
    options={
        'build_exe': {
            'excludes': excludes,
            'packages': ['sip', 'encodings', 'encodings.hex_codec', 'encodings.utf_8'],
            'build_exe': dir_,
            'icon': 'miyamotodata/win_icon.ico',
            },
        },
    executables = [
        Executable(
            'miyamoto.py',
            base = base,
            ),
        ],
    )
print('>> Built frozen executable!')



# Now that it's built, configure everything


if platform.system() == 'Windows':
    # Remove a useless file we don't need
    try: os.unlink(dir_ + '/w9xpopen.exe')
    except: pass
else: pass

print('>> Attempting to copy required files...')
if os.path.isdir(dir_ + '/miyamotodata'): shutil.rmtree(dir_ + '/miyamotodata') 
if os.path.isdir(dir_ + '/miyamotoextras'): shutil.rmtree(dir_ + '/miyamotoextras')
shutil.copytree('miyamotodata', dir_ + '/miyamotodata') 
shutil.copytree('miyamotoextras', dir_ + '/miyamotoextras')
if platform.system() == 'Windows':
    if os.path.isdir(dir_ + '/Tools'): shutil.rmtree(dir_ + '/Tools') 
    shutil.copytree('Tools', dir_ + '/Tools')
    if not os.path.isfile(dir_ + '/libEGL.dll'):
        shutil.copy('libEGL.dll', dir_)
elif platform.system() == 'Linux':
    if os.path.isdir(dir_ + '/linuxTools'): shutil.rmtree(dir_ + '/linuxTools') 
    shutil.copytree('linuxTools', dir_ + '/linuxTools')
else:
    if os.path.isdir(dir_ + '/macTools'): shutil.rmtree(dir_ + '/macTools') 
    shutil.copytree('macTools', dir_ + '/macTools')
shutil.copy('license.txt', dir_)
print('>> Files copied!')

print('>> Miyamoto! has been frozen to %s !' % dir_)

zf = zipfile.ZipFile(PackageName + ".zip", "w", zipfile.ZIP_DEFLATED)
for dirname, subdirs, files in os.walk(dir_):
    zf.write(dirname)
    for filename in files:
        os.path.abspath(os.path.join(dirname, filename))
        zf.write(os.path.join(dirname, filename))
zf.close()
print('Miyamoto! has been packed as zip')
shutil.copy(PackageName + ".zip", "distrib")
