#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#===============================================================================
# CxFreeze setup V0.54, added makeRessources.
#
# Features:
# - NSIS support (Windows installer)
# - PyGTK support
# - Console kicked out
# - NSIS-uninstall works perfect
#
# (c) by Mark Muzenhardt
#===============================================================================

import sys, os, imp


# Catch install-option before this script runs --------------------------------
if len(sys.argv) == 1:
    sys.argv.append('build')
else:
    if sys.argv[1] == "install":
        print "This is a cx-freeze setup, no installation option available!"
        quit()


# Import cx_freeze and the source code ----------------------------------------
from cx_Freeze import setup, Executable
from src.config import *
from src.BaseUI.BuildHelpers import *


python_version = sys.version[:3]
base = "Console"
pathname = os.getcwd()
icon = pathname + '/res/' + APP_ICON


# Build executable ------------------------------------------------------------
if sys.platform.startswith('win32'):
    base = "Win32GUI"
    gtk_dir = get_winGTKdir()
    os.system('del %s\\build\\*.* /S /Q' % pathname)
    build_dir = '\\build\\exe.%s-%s\\' % (sys.platform, python_version)
elif sys.platform.startswith('linux'):
    gtk_dir = None
    os.system('rm -R %s/build/*' % pathname)
    build_dir = '/build/exe.%s-%s/' % (sys.platform, python_version)
else:
    print 'The operating system %s is not supported by this setup!' % sys.platform 
    quit()
    
setup(name = APP_NAME,
      version = APP_VERSION,
      description = APP_DESCRIPTION,
      author = APP_AUTHOR,
      url = APP_URL,
      executables = [Executable('%s.pyw' % APP_NAME, \
                                base = base,
                                icon = icon)])

                                
# Do miscellaneous things -----------------------------------------------------
APP_REVISION = get_revision()
makeAbout(tpl_path='res/about_tpl.svg',
          svg_path='res/about.svg',
          author=APP_AUTHOR,
          version=APP_VERSION, 
          revision=APP_REVISION, 
          license=APP_LICENSE)


# Copy needed GTK and resource files to build dir -----------------------------
if sys.platform == "win32" and sys.argv[1] == "build":
    makeGTK(gtk_dir, pathname, build_dir, LOCALIZED)
    makeRessources(pathname, build_dir)
    makeSphinx(pathname, build_dir)
    makeNSI(pathname, build_dir, APP_NAME, APP_VERSION, APP_ICON)
    
    

