# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS flight_controler module. Completely rewritten in v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

from BaseUI import Portlets
from BaseUI.DB import SQLdb
from BaseUI.GTK import Glade, Dialogs
from config import *

DEBUG = False

if DEBUG:
    from pprint import pprint
    
    
class main:
    def __init__(self, db_object=None):
        self.db_object = db_object
        
        self.wTree = Glade.import_tree(self, RESOURCE_DIR + 'portlets.glade', 'portlet_flight_control')
        self.window = self.wTree.get_widget('portlet_flight_control')
        
        # Cut portlet out of window
        self.portlet = self.window.get_child()
        self.window.remove(self.portlet)
        self.window.destroy()
        
        