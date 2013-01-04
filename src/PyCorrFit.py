#!/usr/bin/python
# -*- coding: utf-8 -*-
""" PyCorrFit
    Paul Müller, Biotec - TU Dresden

    A flexible tool for fitting and analyzing correlation curves.

    Dimensionless representation:
    unit of time        : 1 ms
    unit of inverse time: 1000 /s
    unit of distance    : 100 nm
    unit of Diff.coeff  : 10 um^2/s
    unit of inverse area: 100 /um^2
    unit of inv. volume : 1000 /um^3


    PyCorrFit is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published 
    by the Free Software Foundation, either version 2 of the License, 
    or (at your option) any later version.

    PyCorrFit is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of 
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
    See the GNU General Public License for more details. 

    You should have received a copy of the GNU General Public License 
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import csv
from distutils.version import LooseVersion
import sys
# Import matplotlib a little earlier. This way some problems with saving
# dialogs that are not made by "WXAgg" are solved.


## On Windows XP I had problems with the unicode Characters.
# I found this at 
# http://stackoverflow.com/questions/5419/python-unicode-and-the-windows-console
# and it helped (needs to be done before import of matplotlib):
import platform
if platform.system() == 'Windows':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
import matplotlib
# We do catch warnings about performing this before matplotlib.backends stuff
#matplotlib.use('WXAgg') # Tells matplotlib to use WxWidgets
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    matplotlib.use('WXAgg') # Tells matplotlib to use WxWidgets for dialogs
import numpy as np                  # NumPy
import os
import scipy
try:
    import sympy
except ImportError:
    print "Importing sympy failed! Checking of external model functions"
    print "will not work!"
    # We create a fake module sympy with a __version__ property.
    # This way users can run PyCorrFit without having installed sympy.
    class Fake(object):
        def __init__(self):
            self.__version__ = "0.0 unknown"
            self.version = "0.0 unknown"
    sympy = Fake()
# We must not import wx here. frontend/gui does that. If we do import wx here,
# somehow unicode characters will not be displayed correctly on windows.
# import wx
import yaml

## Continue with the import:
import doc
import frontend as gui              # The actual program




def CheckVersion(given, required, name):
    """ For a given set of versions  str *required* and str *given*,
    where version are usually separated by dots, print whether for
    the module str *name* the required verion is met or not.
    """
    try:
        req = LooseVersion(required)
        giv = LooseVersion(given)
    except:
        print " WARNING: Could not verify version of "+name+"."
        return
    if req > giv:
        print " WARNING: You are using "+name+" v. "+given+\
              " | Required: "+name+" "+ required
    else:
        print " OK: "+name+" v. "+given+" | "+required+" required"


## VERSION
version = doc.__version__
__version__ = version

print gui.doc.info(version)

## Check important module versions
print "\n\nChecking module versions..."
CheckVersion(csv.__version__, "1.0", "csv")
CheckVersion(np.__version__, "1.5.1", "NumPy")
CheckVersion(scipy.__version__, "0.8.0", "SciPy")
CheckVersion(sympy.__version__, "0.7.2", "sympy")
CheckVersion(gui.wx.__version__, "2.8.10.1", "wxPython")
CheckVersion(yaml.__version__, "3.09", "yaml")

## Command line ?


## Start gui
app = gui.wx.App(False)
frame = gui.MyFrame(None, -1, version)
# Before starting the main loop, check for possible session files
# in the arguments.
if hasattr(sys, 'frozen'):
    # Then we are an executable and need to use argument 0
    sysarg = sys.argv
    if len(sysarg) > 1:
        arg = sysarg[1]
    else:
        arg = ""
elif len(sys.argv) >= 2:
    # We have something like "python Scriptname.py argument"
    arg = sys.argv[1]
else:
    arg = ""

if len(arg) >= 18:
    # Send first argument as session file
    print "\nLoading Session "+arg
    frame.OnOpenSession(sessionfile=arg)
elif len(arg) != 0:
    print "\nI do not know what to do with this argument: "+arg
# Now start the app
app.MainLoop()

