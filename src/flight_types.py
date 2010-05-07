# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS options module. Introduced in v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

from BaseUI import Portlets
from BaseUI.DB import SQLdb
from BaseUI.GTK import Glade, Dialogs
from config import *


class main:
    def __init__(self, db_object=None):
        self.db_object = db_object
        self.db_table_flight_types = db_table_flight_types(self.db_object)
        
        self.ui_form = ui_form_flight_types(self.db_object)
        self.ui_table = ui_table_flight_types(self.db_object, self.ui_form)
        
        self.portlet = self.ui_table.portlet
        

        
class db_table_flight_types(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',          'data_type': 'bigint' , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'abbrevation', 'data_type': 'varchar', 'character_maximum_length': 10},
        {'column_name': 'description', 'data_type': 'varchar', 'character_maximum_length': 40}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'flight_types')
        differences_lod = self.check_attributes(self.attributes, add=True)



class ui_form_flight_types(Portlets.Form):
    definition = \
    [
        {'column_name': 'abbrevation', 'widget_name': 'entry_abbrevation'},
        {'column_name': 'description', 'widget_name': 'entry_description'}
    ]

    def __init__(self, db_object):
        self.db_object = db_object
        self.db_table = db_table_flight_types(self.db_object)

        Portlets.Form.__init__(self, icon_file=RESOURCE_DIR + 'flight_types_16.png', title='Flugarten', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_flight_types', help_file='user/options.html')
        self.attributes_lod = self.db_table.attributes
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod='')



class ui_table_flight_types(Portlets.Table):
    definition = \
    [
        {'column_name': 'id',          'column_number': 0, 'visible': False},
        {'column_name': 'abbrevation', 'column_number': 1, 'column_label': 'Kürzel'},
        {'column_name': 'description', 'column_number': 2, 'column_label': 'Beschreibung'}
    ]

    def __init__(self, db_object, form_object):
        self.db_object = db_object
        self.db_table = db_table_flight_types(self.db_object)

        Portlets.Table.__init__(self, form_object, filter=False, help=False, separate_toolbar=False)
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition)

        self.Table.set_sort_column('abbrevation')




