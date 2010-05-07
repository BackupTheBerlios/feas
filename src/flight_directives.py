# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS flight_directives module. Introduced in v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import flight_sectors

from BaseUI import Portlets
from BaseUI.DB import SQLdb
from BaseUI.GTK import Glade, Dialogs
from config import *


class main:
    def __init__(self, db_object=None):
        self.db_object = db_object
        self.db_table_flight_directives = db_table_flight_directives(self.db_object)
        
        self.ui_form = ui_form_flight_directives(self.db_object)
        self.ui_table = ui_table_flight_directives(self.db_object, self.ui_form)
        
        self.portlet = self.ui_table.portlet
            
    

class view:
    # Something must be shown at login!
    def __init__(self, db_object=None):
        self.db_object = db_object
        self.db_table_flight_directives = db_table_flight_directives(self.db_object)
        
     #   self.ui_table = ui_table_sector_permissions
     #   self.portlet = ui_table_sector_permissions.portlet


        
class db_table_flight_directives(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',        'data_type': 'bigint' , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'directive', 'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'note',      'data_type': 'text'},
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'flight_directives')
        differences_lod = self.check_attributes(self.attributes, add=True)



class ui_table_flight_directives(Portlets.Table):
    definition = \
    [
        {'column_name': 'id',          'column_number':  0, 'visible': False},
        {'column_name': 'directive',   'column_number':  1, 'column_label': 'Direktive'},
        {'column_name': 'note',        'column_number':  2, 'column_label': 'Bemerkung'},
    ]

    def __init__(self, db_object, form_object):
        self.db_object = db_object
        self.db_table = db_table_flight_directives(self.db_object)

        Portlets.Table.__init__(self, form_object, filter=False, help=False, separate_toolbar=False)
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition)

        self.Table.set_sort_column('directive')



class ui_form_flight_directives(Portlets.Form):
    def __init__(self, db_object):
        Portlets.Form.__init__(self, icon_file=RESOURCE_DIR + 'dfs_logo_22.png', title='Direktiven', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_flight_directives', help_file='user/flight_directives.html')
        
        self.definition = \
        [
            {'column_name': 'directive',   'widget_name': 'entry_directive'},
            {'column_name': 'note',        'widget_name': 'textview_note'},
        ]
        
        self.db_object = db_object
        self.db_table = db_table_flight_directives(self.db_object)
        
        self.flight_sectors_main = flight_sectors.main(self.db_object, parent_form=self)
        
        self.portlets = \
        [
            {'portlet': self.flight_sectors_main.portlet, 
             'container': 'alignment_flight_sectors',
             'populate_function': self.flight_sectors_main.ui_table.populate,
             'delete_function': self.flight_sectors_main.db_table.delete_directive},
        ]
        
        self.attributes_lod = self.db_table.attributes
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod=self.portlets)



class db_table_flight_directives_fields(SQLdb.table):
    definition = \
    [
        {'column_name': 'id',                       'data_type': 'bigint',  'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'column_name',              'data_type': 'varchar', 'character_maximum_length': 128},
        {'column_name': 'data_type',                'data_type': 'integer'},
        {'column_name': 'character_maximum_length', 'data_type': 'integer'},
        {'column_name': 'numeric_precision',        'data_type': 'integer'},
        {'column_name': 'numeric_scale',            'data_type': 'integer'},
        {'column_name': 'is_nullable',              'data_type': 'bool'},
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'flight_directives_fields')
        differences_lod = self.check_attributes(self.attributes, add=True)
        


