# -*- coding: iso-8859-1 -*-
# Flight calculator v0.1 from 2009-04-14.

from BaseUI.GTK import Glade


class main:
    def __init__(self):
        pass


    # Init class --------------------------------------------------------------
    def initGUIwindow(self):
        self.wTree = Glade.import_tree(self, "main.glade", "window_flight_calculator")
        self.window = self.wTree.get_widget("window_flight_calculator")
        self.window.set_keep_above(True)
        self.window.show_all()
        return



