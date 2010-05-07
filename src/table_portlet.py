# -*- coding: iso-8859-1 -*-
# members modul from: Mark Muzenhardt, beta V0.2 from 2008-05-28

import gtk

from database import *  # surely needed for this module
from functions import * # because of help
#from widgets import *   # because of populating treeview
from config import *    # needed for path-variables etc.


class portlet_table:
    # Button functions --------------------------------------------------------
    #def on_button_add_clicked(self, widget=None):
    #    self.add_dataset()

    def on_button_remove_clicked(self, widget=None):
        '''
        Function triggered by button_remove
        '''
        response = dialog("Frage", label_text="""\
Soll dieser Datensatz entgültig gelöscht werden?
""", dialog_type="question", parent=widget.get_toplevel())

        if response == "APPLY":
            self.remove_dataset()

    def on_button_edit_clicked(self, widget=None):
        '''
        Function triggered by button_edit
        '''
        self.edit_dataset(self.selected_item)

    def on_button_print_preview_clicked(self, widget=None):
        '''
        Function triggered by button print_preview

        Note:
        If function set_print_preview is set, it triggers the object given there
        '''
        if self.print_preview <> None:
            self.print_preview()
        else:
            filename = self.gtk_db_table.build_report()
            startbrowser(filename)

    def on_button_preferences_clicked(self, widget=None):
        '''
        Function triggered by button_preferences
        '''
        self.window_options.initGUIportlet()

    def on_button_help_clicked(self, widget=None):
        '''
        Function triggered by button_help
        '''
        print "Helop!"

    def on_combobox_filter_changed(self, widget=None):
        '''
        If combobox_filter was changed, this function is triggered
        '''
        combobox_filter_model = self.combobox_filter.get_model()
        combobox_item = self.combobox_filter.get_active()
        if combobox_item < 0:
            return None
        item_content = combobox_filter_model[combobox_item][0]

        for list_content in self.filter_function_list:
            if item_content in list_content[0]:
                self.active_filter_function = list_content[1]
        self.gtk_db_table.update_treeview(self.active_filter_function)

    # Widget functions --------------------------------------------------------
    def on_treeview_row_activated(self, widget=None, path=None, column=None):
        '''
        Function triggered if treeview_row is double-clicked
        '''
        selection = widget.get_selection()
        selected_tuple = selection.get_selected()
        selected_tree_iter = selected_tuple[1]
        self.selected_item = self.treeview.get_model().get_value(selected_tree_iter, 0)
        self.edit_dataset(self.selected_item)

    def on_treeview_cursor_changed(self, widget=None, path=None, column=None):
        '''
        Function triggered if a table-row has been selected
        '''
        self.button_remove.set_sensitive(1)
        self.button_edit.set_sensitive(1)

        selection = widget.get_selection()
        selected_tuple = selection.get_selected()
        selected_tree_iter = selected_tuple[1]
        self.selected_item = self.treeview.get_model().get_value(selected_tree_iter, 0)

    # main functions ----------------------------------------------------------
    def add_dataset(self):
        self.button_remove.set_sensitive(0)
        self.button_edit.set_sensitive(0)
        key_number = self.db_table.get_first_key_number()
        self.window_form.edit(key_number, self.treeview, self)

    def remove_dataset(self):
        self.db_table.delete_data(self.selected_item)
        self.gtk_db_table.update_treeview(self.active_filter_function)
        self.button_remove.set_sensitive(0)
        self.button_edit.set_sensitive(0)

    def edit_dataset(self, key_number):
        self.window_form.edit(key_number, self.treeview, self)

    def set_print_preview(self, object):
        '''
        Sets the function which is triggered by button_print_preview
        '''
        self.print_preview = object
        return

    def set_update_function(self, object):
        #self.update_function = object
        self.gtk_db_table.set_update_function(object)
        return

    def get_selected_item(self):
        '''
        Returns the selected table item
        '''
        return self.selected_item

    # Filtering functions -----------------------------------------------------
    def append_filter_function(self, filter_description, filter_function):
        # This sets up the filter_combobox in case it has no model.
        combobox_filter_model = self.combobox_filter.get_model()
        if combobox_filter_model == None:
            liststore = gtk.ListStore(str)
            cell_renderer_text = gtk.CellRendererText()
            self.combobox_filter.pack_start(cell_renderer_text, True)
            self.combobox_filter.add_attribute(cell_renderer_text, 'text', 0)
            self.combobox_filter.set_model(liststore)
            self.filter_function_list.append([unicode("<alle Einträge>", "latin-1"), None])
            self.combobox_filter.append_text(unicode("<alle Einträge>", "latin-1"))
            self.combobox_filter.set_active(0)

        # If the model exists, just append the given values.
        self.filter_function_list.append([unicode(filter_description, "latin-1"), filter_function])
        self.combobox_filter.append_text(unicode(filter_description, "latin-1"))
        return

    def set_combobox_filter(self, active):
        self.combobox_filter.set_active(active)

    def set_sorting_column(self, sort_column=None, sort_ascending=None):
        self.gtk_db_table.set_sorting_column(sort_column, sort_ascending)
        return

    # Treeview functions ------------------------------------------------------
    def update_treeview(self):
        self.gtk_db_table.update_treeview(self.active_filter_function)

    #def populate_treeview_from_db(self, filter_function=None):
    #    self.gtk_db_table.populate_from_db_layout(filter_function)

    def get_toolbar(self):
        self.vbox.remove(self.toolbar)
        return self.toolbar

    # Initialize GUI and class ------------------------------------------------
    def initGUIportlet(self, nowindow=False, search=True, toolbar=True, addremove=True, filter=False):
        self.wTree = import_glade_tree(self, "portlets.glade", "portlet_table")
        self.window = self.wTree.get_widget("portlet_table")
        self.vbox = self.wTree.get_widget("vbox")
        self.scrolledwindow = self.wTree.get_widget("scrolledwindow")

        self.toolbar = self.wTree.get_widget("toolbar")
        if toolbar == False: self.toolbar.hide()
        # ---------------------------------------------------------------------
        self.hbox_dataset = self.wTree.get_widget("hbox_dataset")
        self.button_add = self.wTree.get_widget("button_add")
        self.button_edit = self.wTree.get_widget("button_edit")
        self.button_remove = self.wTree.get_widget("button_remove")
        self.vseparator_dataset = self.wTree.get_widget("vseparator_dataset")
        if addremove == False: self.hbox_dataset.hide()
        # ---------------------------------------------------------------------
        self.hbox_filter = self.wTree.get_widget("hbox_filter")
        self.combobox_filter = self.wTree.get_widget("combobox_filter")
        if filter == False: self.hbox_filter.hide()
        # ---------------------------------------------------------------------
        self.hbox_search = self.wTree.get_widget("hbox_search")
        self.entry_search = self.wTree.get_widget("entry_search")
        self.button_search = self.wTree.get_widget("button_search")
        if search == False: self.hbox_search.hide()
        # ---------------------------------------------------------------------
        self.treeview = self.wTree.get_widget("treeview")
        self.gtk_db_table = gtk_db_table(self.treeview, self.db_table, self.db_table_layout_list)
        #self.gtk_db_table.set_treeview(self.treeview)

        # start populating filter_combobox
        self.filter_function_list = []
        self.active_filter_function= None

        self.gtk_db_table.populate_from_db_layout()

        if nowindow == True:
            self.portlet = self.window.get_child()
            self.window.remove(self.portlet)
            self.window.destroy()
            return self.portlet
        return

    def __init__(self, db_table, window_form=None, editable=False):
        self.db_table = db_table
        self.db_table_layout_list = window_form.db_table_layout()

        self.window_form = window_form
        self.window_options = window_options()

        self.selected_item = None
        self.print_preview = None
        self.update_function = None


class window_form:
    def __init__(self, db_table, db_table_layout, portlet_list=None):
        ''' portlet_list[portlet_to_add, container, update_function, save_function]
                portlet_to_add = widget to add in the container
                container = the widget_name of the gtk container which contains the portlet_to_add
                update_function = function to trigger in case of edit a dataset
                save_function = function to trigger in case of saving a dataset'''

        self.db_table = db_table
        self.db_table_layout = db_table_layout
        self.portlet_list = portlet_list
        return

    # Widget functions --------------------------------------------------------
    def on_button_ok_clicked(self, widget=None):
        if self.db_table.key_number_exists(self.key_number):
            self.db_table.update_data(self.key_number, self.db_table_layout_list)
        else:
            self.db_table.insert_data(self.db_table_layout_list)

        self.portlet_table.update_treeview()

        # Do all save functions given in the portlet list
        if self.portlet_list <> None:
            number_of_portlets = len(self.portlet_list)
            for portlet_number in xrange(number_of_portlets):
                if self.portlet_list[portlet_number][3] <> None:
                    save_function = self.portlet_list[portlet_number][3]()
        self.window.destroy()
        return

    def on_togglebutton_calendar_toggled(self, widget=None):
        print "calendar from", widget
        self.window.set_keep_above(False)

        fixed = widget.get_parent()
        table = fixed.get_parent()
        children = table.get_children()

        for widget_object in children:
            widget_name = widget_object.get_name()
            if widget_name[0:5] == "entry":
                entry = widget_object

        if widget.get_active() == 1:
            calendar = dialog_calendar()
            calendar.initGUI_calendar("SE", widget, entry, parent=self.window)

    def on_button_cancel_clicked(self, widget=None):
        self.window.destroy()
        return

    def on_button_help_clicked(self, widget=None):
        helpfile_name = DOCUMENTATION_DIR + self.db_table.get_name() + ".html"
        print helpfile_name

        startbrowser(helpfile_name, self.window)
        return

    def on_textview_key_pressed(self, widget=None, event=None, column=None):
        text_buffer = widget.get_buffer()
        start_iter = text_buffer.get_start_iter()
        end_iter = text_buffer.get_end_iter()
        # TODO: Here should be prooves on correct entry

    def on_widget_changed(self, widget=None, column=None):
        entry_validity = True
        if self.db_table_layout_list[column].has_key('db_field_type'):
            db_field_type = self.db_table_layout_list[column]['db_field_type']
        else:
            db_field_type = ''

        db_column_name = self.db_table_layout_list[column]['db_field_name']

        if self.db_table_layout_list[column].has_key('gtk_widget_name'):
            widget_name = self.db_table_layout_list[column]['gtk_widget_name']
        else:
            widget_name = ''

        widget_content = widget.get_text()

        # Check valid length of entry on varchar
        if db_field_type.startswith("varchar"):
            max_field_length = int(db_field_type[db_field_type.find("(")+1:db_field_type.find(")")])
            entry_string_length = len(widget.get_text())
            if entry_string_length > max_field_length:
                entry_validity = False
            else:
                entry_validity = True

        # Check validity of integers in entrys
        if db_field_type.startswith("integer") or db_field_type.startswith("bigint"):
            try:
                dummy = int(widget_content)
                entry_validity = True
            except:
                entry_validity = False

        # Check validity of date-fields
        if db_field_type.startswith("date"):
            entry_validity = validate_datestring(widget_content)

        # Check validity of time-fields:
        if db_field_type.startswith("time"):
            entry_validity = validate_timestring(widget_content)

        # Set widget background red if entry is not valid!
        if entry_validity == True:
            set_white(widget)
            self.button_ok.set_sensitive(1)
            self.set_all_entrys_sensitivity(1, widget_name)
        else:
            set_red(widget)
            self.button_ok.set_sensitive(0)
            self.set_all_entrys_sensitivity(0, widget_name)

    def on_window_destroy(self, widget=None):
        # Remove portlets safely from the containers, so they can be re-used!
        if self.portlet_list <> None:
            number_of_portlets = len(self.portlet_list)
            for portlet_number in xrange(number_of_portlets):
                if self.portlet_list[portlet_number][1] <> None:
                    container = self.wTree.get_widget(self.portlet_list[portlet_number][1])
                    child = container.get_child()
                    if child <> None:
                        container.remove(child)
        return

    # Main functions ----------------------------------------------------------
    def set_all_entrys_sensitivity(self, sensitivity, except_widget_name=None):
        """Just sets the sensitivity of all entrys from a self.db_table_layout_list
           excepting the one given on except_widget_name."""

        number_of_widgets = len(self.db_table_layout_list)
        for widget_number in xrange(number_of_widgets):
            layout_dict = self.db_table_layout_list[widget_number]

            if layout_dict.has_key('gtk_widget_name'):
                if layout_dict['gtk_widget_name'] <> except_widget_name and layout_dict['gtk_widget_name'] <> None:
                    if layout_dict.has_key('gtk_widget_object') and layout_dict['gtk_widget_object'] <> None:
                        if layout_dict['gtk_widget_name'].startswith("entry"):
                            layout_dict['gtk_widget_object'].set_sensitive(sensitivity)
                        if layout_dict['gtk_widget_name'].startswith("comboboxentry"):
                            layout_dict['gtk_widget_object'].child.set_sensitive(sensitivity)
        return

    def populate_form_from_db(self):
        column_dictlist = self.db_table.filter("pk_key_number = " + str(self.key_number))[0]
        number_of_fields = len(self.db_table_layout_list)

        for field_number in xrange(number_of_fields):
            column_dict = self.db_table_layout_list[field_number]
            # This is needed if no gtk_widget_object is given in dict!
            if column_dict.has_key('gtk_widget_object'):
                widget = column_dict['gtk_widget_object']
            else:
                widget = None

            # This gets the widget_content from own- and foreign-fields.
            if column_dict.has_key('db_foreign_key_column'):
                DBcnx = self.db_table.get_DBcnx()
                foreign_db_table = db_table(DBcnx, column_dict['db_foreign_table'])
                widget_content = foreign_db_table.get_foreign_cell_text(column_dictlist[column_dict['db_field_name']], column_dict['db_foreign_key_column'], foreign_db_table, column_dict['db_foreign_field_name'])
            else:
                widget_content = column_dictlist[column_dict['db_field_name']]

            # This is needed to set foreign key fields to bigint!
            if column_dict.has_key('db_field_type'):
                db_field_type = column_dict['db_field_type']
            if column_dict.has_key('db_foreign_field_name'):
                db_field_type = 'bigint'

            if widget == None:
                if DEBUG: print "Layout entry " + str(column_dict) + " has no widget!"

            # Convert date to european format if necessary.
            if db_field_type.startswith("date") and widget_content <> None:
                if len(widget_content) >= 10:
                    year = widget_content[0:4]
                    month = widget_content[5:7]
                    day = widget_content[8:10]
                    widget_content = day + "." + month + "." + year

            # Just populate all kind of widgets with table content
            if widget_content <> None and widget <> None:
                if widget.get_name().startswith("entry"):
                    widget.set_text(unicode(str(widget_content), "latin-1"))
                if widget.get_name().startswith("comboboxentry"):
                    widget.child.set_text(str(widget_content))

                    # This is the magic which populates a comboboxentry list from foreign column!
                    if column_dict.has_key('db_foreign_key_column'):
                        foreign_columns_list = []
                        foreign_pk_list = foreign_db_table.get_column('pk_key_number')
                        for foreign_pk in foreign_pk_list:
                            foreign_data = foreign_db_table.search_column('pk_key_number', foreign_pk, column_dict['db_foreign_field_name'])[0]
                            foreign_columns_list.append([foreign_pk, foreign_data])
                        populate_comboboxentry_from_list(widget, foreign_columns_list, key_column=True)

                if widget.get_name().startswith("check"):
                    if widget_content == "f":
                        widget.set_active(False)
                    if widget_content == "t":
                        widget.set_active(True)
                if widget.get_name().startswith("textview"):
                    text_buffer = widget.get_buffer()
                    text_buffer.set_text(unicode(str(widget_content), "latin-1"))
        return

    def edit(self, key_number, treeview, portlet_table):
        self.initGUIwindow()
        self.key_number = key_number
        self.treeview_portlet = treeview
        self.portlet_table = portlet_table

        self.entry_key_number = get_widget_from_db_table_layout(self.db_table_layout_list, "entry_key_number")
        if self.entry_key_number <> None:
            self.entry_key_number.set_text(str(key_number))

        if self.db_table.key_number_exists(key_number):
            self.populate_form_from_db()

        # Do all update fuctions given in the portlet list
        if self.portlet_list <> None:
            number_of_portlets = len(self.portlet_list)
            for portlet_number in xrange(number_of_portlets):
                if self.portlet_list[portlet_number][2] <> None:
                    save_function = self.portlet_list[portlet_number][2](self.db_table_layout_list)
        return

    def get_widget(self, widget_name):
        widget = self.wTree.get_widget(widget_name)
        return widget

    def initGUIwindow(self, nowindow=False):
        '''Shows the Form window and creates widget connections
           nowindow = True:  removes the window container and returns only the window-child
                      False: opens window normally'''

        self.wTree = import_glade_tree(self, "forms.glade", "window_" + self.db_table.get_name())
        self.window = self.wTree.get_widget("window_" + self.db_table.get_name())
        self.window.connect("destroy", self.on_window_destroy)
        self.window.set_keep_above(True)

        self.button_ok = self.wTree.get_widget("button_ok")

        # Associates the widget objects with self.db_table_layout_table
        self.db_table_layout_list = self.db_table_layout()
        number_of_columns = len(self.db_table_layout_list)
        for column_number in xrange(number_of_columns):
            if self.db_table_layout_list[column_number].has_key('gtk_widget_name'):
                widget_name = self.db_table_layout_list[column_number]['gtk_widget_name']
            else:
                widget_name = None

            if widget_name <> None:
                self.db_table_layout_list[column_number]['gtk_widget_object'] = self.wTree.get_widget(self.db_table_layout_list[column_number]['gtk_widget_name'])
                if self.db_table_layout_list[column_number]['gtk_widget_object'] <> None:
                    # Connect the changed-signal to all entry-widgets to verify the content!
                    if widget_name.startswith("entry"):
                        self.db_table_layout_list[column_number]['gtk_widget_object'].connect("changed", self.on_widget_changed, column_number)
                    if widget_name.startswith("comboboxentry"):
                        self.db_table_layout_list[column_number]['gtk_widget_object'].child.connect("changed", self.on_widget_changed, column_number)
                    if widget_name.startswith("textview"):
                        self.db_table_layout_list[column_number]['gtk_widget_object'].connect("key-press-event", self.on_textview_key_pressed, column_number)

        # Packs the widget(s) to add in the container(s) if portlet_list is not empty
        if self.portlet_list <> None:
            number_of_portlets = len(self.portlet_list)
            for portlet_number in xrange(number_of_portlets):
                widget = self.portlet_list[portlet_number][0](self.db_table_layout_list)
                if widget <> None:
                    widget.show()
                if self.portlet_list[portlet_number][1] <> None:
                    container = self.wTree.get_widget(self.portlet_list[portlet_number][1])
                    container.add(widget)
                    if DEBUG: print "container_child:", container.get_child()

        if nowindow == True:
            portlet = self.window.get_child()
            self.window.remove(portlet)
            self.window.destroy()
            return portlet
        return


class window_options:
    def __init__(self):
        pass

    # Init class --------------------------------------------------------------
    def initGUIportlet(self):
        self.wTree = import_glade_tree(self, "forms.glade", "window_table_options")
        self.window = self.wTree.get_widget("window_table_options")
        self.window.set_keep_above(True)
        return


class gtk_db_table:
    def __init__(self, treeview, db_table, db_table_layout):
        self.db_table = db_table
        self.db_table_layout = db_table_layout
        self.treeview = treeview

        self.table_dict = {}
        self.sort_column = None
        self.sort_ascending = True
        self.update_function = None

    def update_treeview(self, filter_function=None):
        number = 1
        while number > 0:
            column = self.treeview.get_column(0)
            if column <> None:
                number = self.treeview.remove_column(column)
            else:
                number = 0
        self.populate_from_db_layout(filter_function)

        if self.sort_column <> None:
            self.sort_liststore(self.sort_column)

        if self.update_function <> None:
            self.update_function()
        return

    def set_sorting_column(self, sort_column=None, sort_ascending=None):
        self.sort_ascending = sort_ascending
        self.sort_column = self.sort_liststore(sort_column)
        return

    def sort_liststore(self, column):
        '''
        sorts the entire liststore with following args:
            column = column number to sort
            ascending = True: Sort ascending / False: Sort descending
        '''

        if self.sort_ascending == True: algorithm = gtk.SORT_ASCENDING
        if self.sort_ascending == False: algorithm = gtk.SORT_DESCENDING

        self.liststore.set_default_sort_func(lambda *args: column)
        self.liststore.set_sort_column_id(column, algorithm)
        return column

    def build_report(self):
        HTMLtable = self.db_table.convert_to_html(self.db_table_layout)
        filename = "tmp\\" + self.db_table.get_name() + ".html"

        #filename = fileselection("Speichern...", gtk.FILE_CHOOSER_ACTION_SAVE)
        if filename <> None:
            HTMLfile = open(filename ,"w")
            HTMLfile.write(HTMLheader(title=self.db_table.get_name(), body=HTMLtable))
            HTMLfile.close()
        else:
            if DEBUG: print "Fileselection aborted!"
        return filename

    def populate_from_db_layout(self, filter_function=None, editable=False):
        # Lookup if the db is in sync with the needs of out db_fields_layout and fix it if not.
        if filter_function == None:
            self.table_dict = self.db_table.verify(self.db_table_layout)
        else:
            self.table_dict = self.db_table.filter(filter_function)

        self.populate_columns()
        self.populate_rows()
        return

    def populate_columns(self):
        type_list = []
        treeview_column_list = []

        # First off, the columns has to be sorted in given order.
        self.db_table_layout.sort(compare_by ('gtk_treeview_column'))

        if self.sort_column <> None:
            self.sort_liststore(self.sort_column)

        # This makes the column-setup for the treeview
        column_number = 0
        for column_dict in self.db_table_layout:
            if column_dict.has_key('db_field_type'):
                if column_dict['db_field_type'].startswith("varchar"):
                    entry_type = str
                if column_dict['db_field_type'].startswith("money"):
                    entry_type = str
                if column_dict['db_field_type'].startswith("date"):
                    entry_type = str
                if column_dict['db_field_type'].startswith("time"):
                    entry_type = str
                if column_dict['db_field_type'].startswith("integer"):
                    entry_type = int
                if column_dict['db_field_type'].startswith("float"):
                    entry_type = float
                if column_dict['db_field_type'].startswith("bigint"):
                    entry_type = int
                if column_dict['db_field_type'].startswith("bool"):
                    entry_type = bool

            if column_dict.has_key('db_foreign_field_name'):
                entry_type = str

            type_list += [entry_type]

            # If no column_title entry is found in column_dict, name it like db_field_name.
            if column_dict.has_key('column_title'):
                column_title = unicode(column_dict['column_title'], "latin-1")
            else:
                column_title = unicode(column_dict['db_field_name'], "latin-1")

            # The next question is, if the content of a column is bool or not. If yes, it will be displayed as gtk.CheckButton.
            if entry_type <> bool:
                cell_renderer_text = gtk.CellRendererText()
                if column_dict.has_key('gtk_treeview_column_editable'):
                    cell_renderer_text.set_property('editable', column_dict['gtk_treeview_column_editable'])
                treeview_column_list.append(gtk.TreeViewColumn(column_title, cell_renderer_text, text=column_number))
            else:
                cell_renderer_toggle = gtk.CellRendererToggle()
                treeview_column_list.append(gtk.TreeViewColumn(column_title, cell_renderer_toggle))
                treeview_column_list[column_number].add_attribute(cell_renderer_toggle, "active", column_number)

            self.treeview.append_column(treeview_column_list[column_number])
            treeview_column_list[column_number].set_resizable (True)
            treeview_column_list[column_number].set_sort_column_id (column_number)

            if column_dict.has_key('gtk_column_hide'):
                if column_dict['gtk_column_hide'] == True:
                    treeview_column_list[column_number].set_visible(0)
            column_number += 1

        # TODO: Check this try statement if needed!
        try:
            self.liststore = gtk.ListStore(*type_list)
        except Exception, inst:
            self.liststore = gtk.ListStore(str)

    def populate_rows(self):
        # This finds the right positions for the content.
        number_of_rows = len(self.table_dict)
        for row_number in xrange(number_of_rows):
            row_content = []
            for column_dict in self.db_table_layout:
                column_content = self.table_dict[row_number][column_dict['db_field_name']]
                if column_dict.has_key('db_field_type'):
                    if column_content <> None:
                        if column_dict['db_field_type'].startswith("varchar"):
                            # On text content, encode it to latin-1 for middle-european string-charakters.
                            column_content = unicode(column_content, "latin-1")
                        if column_dict['db_field_type'].startswith("money"):
                            # On money content, encode it to latin-1 for middle-european string-charakters.
                            column_content = unicode(str(column_content), "latin-1")
                        if column_dict['db_field_type'].startswith("time"):
                            # On time content, encode it to latin-1 for middle-european string-charakters.
                            column_content = unicode(str(column_content), "latin-1")
                        if column_dict['db_field_type'].startswith("date"):
                            # On date content, encode it to latin-1 for middle-european string-charakters.
                            usdate_str = unicode(str(column_content), "latin-1")
                            column_content = convert_usdate_to_gmdate(usdate_str)
                        if column_dict['db_field_type'].startswith("integer"):
                            # On integer content, let the column_content integer, too.
                            column_content = column_content
                        if column_dict['db_field_type'].startswith("float"):
                            # On float content, let the column_content integer, too.
                            column_content = column_content
                        if column_dict['db_field_type'].startswith("bigint"):
                            # On bigint content, let the column_content integer, too.
                            column_content = column_content
                        if column_dict['db_field_type'].startswith("bool"):
                            # On boolean content, just make the column_content a bool value to set the gtk.CheckButton's.
                            if column_content == "t":
                                column_content = True
                            if column_content == "f":
                                column_content = False
                    else:
                        if column_dict['db_field_type'].startswith("bool"):
                            column_content = False
                        elif column_dict['db_field_type'].startswith("integer"):
                            column_content = 0
                        elif column_dict['db_field_type'].startswith("float"):
                            column_content = 0.0
                        else:
                            column_content = ""
                elif column_dict.has_key('db_foreign_field_name'):
                    if column_content <> None:
                        DBcnx = self.db_table.get_DBcnx()
                        foreign_db_table = db_table(DBcnx, column_dict['db_foreign_table'])
                        foreign_column_content = foreign_db_table.search_column("pk_key_number", column_content, column_dict['db_foreign_field_name'])[0]
                        if foreign_column_content <> ():
                            column_content = unicode(str(foreign_column_content), "latin-1")
                        else:
                            column_content = "-"
                else:
                    column_content = ""
                row_content += [column_content]

            try:
                self.liststore.append(row_content)
            except Exception, inst:
                print inst

        self.treeview.set_model(self.liststore)
        return

    def set_update_function(self, object):
        self.update_function = object


