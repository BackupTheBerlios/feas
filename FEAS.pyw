#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#===============================================================================
# Application starter V0.8.
# (c) by Mark Muzenhardt
#===============================================================================

import sys
from src.config import *


# Imports for cx_freeze -------------------------------------------------------
import encodings, encodings.ascii, encodings.utf_8, encodings.utf_16_le, \
       encodings.iso8859_1, encodings.iso8859_15, \
       encodings.latin_1


# Import GTK and main module --------------------------------------------------
try:
    import gtk, atk
    import gtk.glade, gtk._gtk, gtk.gdk
    import cairo, pango, pangocairo
except Exception, inst:
    print "Error while importing GTK library,", str(inst)

try:
    from src import main
except Exception, inst:
    print "Error while importing the main application,", str(inst)
    raise
    
    
# Import pyGTK ----------------------------------------------------------------
try:
    import pygtk
    pygtk.require ('2.0')
except Exception, inst:
    print "You must install PyGTK 2.0 to run this programm,", str(inst)


# Check command line arguments ------------------------------------------------
def check_arguments():
    for argument in sys.argv:
        if "debug" in argument:
            print "debugging mode, exiting happily."
            debug_app()
            return False

        if "help" in argument:
            help_app()
            return False

    number_of_arguments = len(sys.argv)
    if number_of_arguments == 1:
        return True
    else:
        print "Invalid arguments. Give -help for manual." + "\n"
        help_app()
        return False


# Check command line arguments ------------------------------------------------
def start_app():
    main.application()
    gtk.main()
    return 0


def debug_app():
    print "debug"


def help_app():
    # Begin console manual...
    print '''\
USAGE:
    --help        shows this text
    --debug       debug mode

NOTE:
    If there are no arguments given,
    this application will simply start.
'''


# Startup if everything is all right ------------------------------------------
start_offset = check_arguments()

if start_offset:
    if __name__ == "__main__":
        start_app()


# Exit properly ---------------------------------------------------------------

# The next lines are needed to prevent the console from closing.
#print "Give <RETURN> to exit..."
#sys.stdin.readline()

print "Application terminated properly!"


