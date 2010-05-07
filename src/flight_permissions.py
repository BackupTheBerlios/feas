# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS flight_directives module. Introduced in v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import gtk

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
        
        self.wTree = Glade.import_tree(self, RESOURCE_DIR + 'portlets.glade', 'portlet_flight_permissions')
        self.window = self.wTree.get_widget('portlet_flight_permissions')
        
        # Cut portlet out of window
        self.portlet = self.window.get_child()
        self.window.remove(self.portlet)
        self.window.destroy()
        


class ui_portlet_flight_permissions(Portlets.Form):
    def __init__(self):
        pass

    
    
class ui_table_flight_permissions(Portlets.Table):
    def __init__(self, flight_directive_id):
        definition = ''
    


class db_table_flight_permissions(SQLdb.table):
    def __init__(self, db_object):
        self.definition = \
        [
            {}
        ]
        
        SQLdb.table.__init__(self, db_object, 'flight_directives_fields')
        differences_lod = self.check_attributes(self.attributes, add=True)
        