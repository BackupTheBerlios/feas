# -*- coding: iso-8859-1 -*-


import gobject, gtk
import time
import table_portlet

from database import *
#from widgets import *
from functions import *
from config import *

class main:
    def __init__(self):
        pass

    def on_treeview_menu_cursor_changed(self, widget, data=None):
        selection = widget.get_selection()
        selected_tuple = selection.get_selected()
        selected_tree_iter = selected_tuple[1]
        self.selected_item = unicode(widget.get_model().get_value(selected_tree_iter, 1), "utf-8").encode("latin-1")

        self.button_ok.set_sensitive(1)
        return

    def on_button_ok_clicked(self, widget=None):
        for item in self.function_list:
            if item[1] == self.selected_item:
                table_name, HTML_body = item[0](self.from_date, self.to_date)
                self.build_HTML_report(table_name, HTML_body)
        self.window.destroy()

    def on_button_cancel_clicked(self, widget=None):
        self.window.destroy()

    def on_entry_from_date_changed(self, widget=None, data=None):
        self.from_date = self.entry_from_date.get_text()

    def on_entry_to_date_changed(self, widget, data=None):
        self.to_date = self.entry_to_date.get_text()

    def on_filechooserbutton_update_preview(self, widget=None, event=None):
        print widget, event
        print event.type
        print dir(event)

    def on_togglebutton_calendar_toggled(self, widget=None):
        # TODO: Cleanup this mess, don't repeat yourselve!
        # print "calendar from", widget
        self.window.set_keep_above(False)

        fixed = widget.get_parent()
        table = fixed.get_parent()
        children = table.get_children()

        for widget_object in children:
            widget_name = widget_object.get_name()
            if widget_name[0:5] == "entry":
                entry = widget_object
                # print entry

        if widget.get_active() == 1:
            calendar = dialog_calendar()
            calendar.initGUI_calendar("SE", widget, entry, parent=self.window)

    def append_function_on_selection(self, function, selection):
        self.function_list.append([function, selection])

    def build_HTML_report(self, table_name, HTML_body):
        #HTMLtable = self.db_table.convert_to_html(self.db_table_layout)
        filename = "tmp\\" + table_name + ".html"

        #filename = fileselection("Speichern...", gtk.FILE_CHOOSER_ACTION_SAVE)
        if filename <> None:
            HTMLfile = open(filename ,"w")
            HTMLfile.write(HTMLheader(title=table_name, body=HTML_body))
            HTMLfile.close()
        else:
            if DEBUG: print "Fileselection aborted!"
        startbrowser(filename)
        return filename

    # Init class --------------------------------------------------------------
    def initGUIportlet(self, menu_layout):
        self.wTree = import_glade_tree(self, "main.glade", "window_report")
        self.window = self.wTree.get_widget("window_report")
        self.window.set_keep_above(True)

        # self.entry_from_date = self.wTree.get_widget("entry_from_date")
        self.function_list = []
        self.treeview_menu = self.wTree.get_widget("treeview_menu")
        self.button_ok = self.wTree.get_widget("button_ok")
        make_treeview_menu(self.treeview_menu, menu_layout)

        self.entry_from_date = self.wTree.get_widget("entry_from_date")
        self.entry_to_date = self.wTree.get_widget("entry_to_date")

        self.from_date = get_gmdate_str()
        self.entry_from_date.set_text(self.from_date)
        self.to_date = get_gmdate_str()
        self.entry_to_date.set_text(self.to_date)

        self.selected_item = None
        return



