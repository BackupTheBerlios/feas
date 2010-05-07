# -*- coding: iso-8859-1 -*-
# report modul from: Mark Muzenhardt, early beta V0.1

#import gtk
import table_portlet

from database import *
#from functions import *
#from widgets import *
#from config import *


class main:
    db_table_licenses_definition = \
    [
        {'db_field_name': 'pk_key_number', 'db_field_type': 'bigint'     ,  'gtk_widget_name': 'entry_key_number'  , 'gtk_treeview_column': 0, 'print_table_column': 0, 'db_primary_key': True, 'gtk_column_hide': True},
        {'db_field_name': 'license_name' , 'db_field_type': 'varchar(40)',  'gtk_widget_name': 'entry_license_name', 'gtk_treeview_column': 1, 'print_table_column': 1, 'column_title': 'Lizenzbezeichnung'},
        {'db_field_name': 'note'         , 'db_field_type': 'varchar(40)',  'gtk_widget_name': 'entry_note'        , 'gtk_treeview_column': 2, 'print_table_column': 2, 'column_title': 'Bemerkung'}
    ]

    # Main functions ----------------------------------------------------------
    def get_portlet(self):
        portlet = self.table_portlet.initGUIportlet(nowindow=True)
        self.table_portlet.set_sorting_column(1, True)
        return portlet

    def get_toolbar(self):
        toolbar = self.table_portlet.get_toolbar()
        return toolbar

    # Widget functions --------------------------------------------------------
    def form_portlet_layout(self):
        portlet_list = []
        #portlet_list.append([self.pack_treeview_content, "scrolledwindow_license_data", None, None])
        return portlet_list

    # Dictionary database declaration -----------------------------------------
    def db_table_layout(self):
        db_table_layout_list = []

        db_table_layout_list.append({'db_field_name': 'pk_key_number', 'db_field_type': 'bigint'     ,  'gtk_widget_name': 'entry_key_number'  , 'gtk_treeview_column': 0, 'print_table_column': 0, 'db_primary_key': True, 'gtk_column_hide': True})
        db_table_layout_list.append({'db_field_name': 'license_name' , 'db_field_type': 'varchar(40)',  'gtk_widget_name': 'entry_license_name', 'gtk_treeview_column': 1, 'print_table_column': 1, 'column_title': 'Lizenzbezeichnung'})
        db_table_layout_list.append({'db_field_name': 'note'         , 'db_field_type': 'varchar(40)',  'gtk_widget_name': 'entry_note'        , 'gtk_treeview_column': 2, 'print_table_column': 2, 'column_title': 'Bemerkung'})
        return db_table_layout_list

    def __init__(self, DBcnx):
        self.db_table_licenses = db_table(DBcnx, 'licenses')
        self.form_window = table_portlet.window_form(self.db_table_licenses, self.db_table_layout, self.form_portlet_layout())
        self.table_portlet = table_portlet.portlet_table(self.db_table_licenses, self.form_window)




