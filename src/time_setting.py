# -*- coding: iso-8859-1 -*-
import gtk

#from widgets import *
from config import *

class portlet_time_setting:
    # This is crap, only for example
    def on_button_copy_clicked(self, widget=None):
        #TODO: Replace by useful breaks...
        pass
        
    # -------------------------------------------------------------------------

    def initGUI(self, nowindow=False):
        self.wTree = import_glade_tree(self, "main.glade", "portlet_time_setting")
        self.window = self.wTree.get_widget("portlet_time_setting")
        
        if nowindow == True:
            self.portlet = self.window.get_child()
            self.window.remove(self.portlet)
            self.window.destroy()
            return self.portlet
        return

    def __init__(self):
        pass
