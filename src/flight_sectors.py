# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS flight_sectors module. Completely rewritten in v0.8 alpha.
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
    def __init__(self, db_object=None, parent_form=None):
        self.db_object = db_object
        self.db_table = db_table_flight_sectors(self.db_object)
        
        self.ui_form = ui_form_flight_sectors(self.db_object, parent_form)
        self.ui_table = ui_table_flight_sectors(self.db_object, self.ui_form, parent_form)
        
        self.portlet = self.ui_table.portlet



class db_table_flight_sectors(SQLdb.table):
    def __init__(self, db_object=None):
        self.attributes = \
        [
            {'column_name': 'id',                  'data_type': 'bigint', 'is_nullable': False, 'is_primary_key': True},
            {'column_name': 'fk_flight_directive', 'data_type': 'bigint', 'referenced_table_name': 'flight_directives', 'referenced_column_name': 'id'},
            {'column_name': 'abbrevation',         'data_type': 'varchar', 'character_maximum_length': 40},
            {'column_name': 'note',                'data_type': 'varchar', 'character_maximum_length': 40},
            {'column_name': 'has_min_alt',         'data_type': 'bool'},
            {'column_name': 'standard_min_value',  'data_type': 'integer'},
            {'column_name': 'has_max_alt',         'data_type': 'bool'},
            {'column_name': 'standard_max_value',  'data_type': 'integer'},
            {'column_name': 'activatable',         'data_type': 'bool'},
            {'column_name': 'deactivated',         'data_type': 'bool'},
        ]
        
        SQLdb.table.__init__(self, db_object, 'flight_sectors')
        differences_lod = self.check_attributes(self.attributes, add=True)


    def delete_directive(self, id):
        self.delete('fk_directive', id)



class ui_table_flight_sectors(Portlets.Table):
    def __init__(self, db_object=None, form_object=None, parent_form=None):
        self.definition = \
        [
            {'column_name': 'id',                 'column_number': 0, 'visible': False},
            {'column_name': 'abbrevation',        'column_number': 1, 'column_label': 'Kürzel'},
            {'column_name': 'note',               'column_number': 2, 'column_label': 'Beschreibung'},
            {'column_name': 'has_min_alt',        'column_number': 3, 'column_label': 'min. Höhe?'},
            {'column_name': 'standard_min_value', 'column_number': 4, 'column_label': 'Standard'},
            {'column_name': 'has_max_alt',        'column_number': 5, 'column_label': 'max. Höhe?'},
            {'column_name': 'standard_max_value', 'column_number': 6, 'column_label': 'Standard'},
            {'column_name': 'activatable',        'column_number': 7, 'column_label': 'aktivierbar?'},
            {'column_name': 'deactivated',        'column_number': 8, 'visible': False},
        ]        
        
        self.db_object = db_object
        self.db_table = db_table_flight_sectors(self.db_object)

        Portlets.Table.__init__(self, form_object, parent_form, filter=False, help=False, separate_toolbar=False)
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition)

        self.Table.set_sort_column('abbrevation')
    
    
    
class ui_form_flight_sectors(Portlets.Form):
    def __init__(self, db_object, parent_form=None):
        self.definition = \
        [
            {'column_name': 'id',                 'widget_name': 'entry_key_number'        , 'gtk_treeview_column': None, 'print_table_column': None, 'db_primary_key': True},
            {'column_name': 'abbrevation',        'widget_name': 'entry_sector_abbrevation', 'gtk_treeview_column':    1, 'print_table_column':    1, 'column_title': 'Sektorenkürzel'},
            {'column_name': 'note',               'widget_name': 'entry_note'              , 'gtk_treeview_column':    2, 'print_table_column':    2, 'column_title': 'Bezeichnung'},
            {'column_name': 'has_min_alt',        'widget_name': 'checkbutton_has_min_alt' , 'gtk_treeview_column':    3, 'print_table_column':    3, 'column_title': 'hat Mindesthöhe'},
            {'column_name': 'standard_min_value', 'widget_name': 'entry_standard_min_value', 'gtk_treeview_column':    4, 'print_table_column':    4, 'column_title': 'Standardwert'},
            {'column_name': 'has_max_alt',        'widget_name': 'checkbutton_has_max_alt' , 'gtk_treeview_column':    5, 'print_table_column':    5, 'column_title': 'hat max. Höhe'},
            {'column_name': 'standard_max_value', 'widget_name': 'entry_standard_max_value', 'gtk_treeview_column':    6, 'print_table_column':    6, 'column_title': 'Standardwert'},
            {'column_name': 'activatable',        'widget_name': 'checkbutton_activatable' , 'gtk_treeview_column':    7, 'print_table_column':    7, 'column_title': 'aktivierbar'},
            {'column_name': 'deactivated',        'widget_name': 'checkbutton_deactivated' , 'gtk_treeview_column': None, 'print_table_column': None}
        ]
                
        self.db_object = db_object
        self.db_table = db_table_flight_sectors(self.db_object)

        Portlets.Form.__init__(self, parent_form, icon_file=RESOURCE_DIR + 'sectors_16.png', title='Flugsektoren', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_flight_sectors', help_file='user/flight_sectors.html')
        self.attributes_lod = self.db_table.attributes
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod='')
        
        
        






