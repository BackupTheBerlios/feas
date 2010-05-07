# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS user_group module. Introduced in v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

from BaseUI import Portlets
from BaseUI.DB import SQLdb
from config import *


class main:
    def __init__(self, db_object=None):
        self.db_object = db_object
        self.db_table = db_table(self.db_object)

        self.ui_form = ui_form(self.db_object)
        self.ui_table = ui_table(self.db_object, self.ui_form)

        self.portlet = self.ui_table.portlet
        self.toolbar = self.ui_table.toolbar


    def get_portlet(self):
        return self.portlet


    def get_toolbar(self):
        return self.toolbar



class db_table(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',          'data_type': 'bigint',  'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'user_group',  'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'description', 'data_type': 'text'},
        {'column_name': 'password',    'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'created',     'data_type': 'timestamp'},
        {'column_name': 'updated',     'data_type': 'timestamp'},
        {'column_name': 'deactivated', 'data_type': 'bool'}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'user_group')
        differences_lod = self.check_attributes(self.attributes, add=True)



class ui_form(Portlets.Form):
    definition = \
    [
        {'column_name': 'user_group',  'widget_name': 'entry_user_group'},
        {'column_name': 'password',    'widget_name': 'entry_password'},
        {'column_name': 'description', 'widget_name': 'textview_description'},
        {'column_name': 'created',     'widget_name': None},
        {'column_name': 'updated',     'widget_name': None},
        {'column_name': 'deactivated', 'widget_name': None},
    ]

    def __init__(self, db_object):
        self.db_object = db_object
        self.db_table = db_table(self.db_object)

        Portlets.Form.__init__(self, icon_file=RESOURCE_DIR + 'member_16.png', title='Benutzergruppen', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_user_group', help_file='user/user_group.html')
        self.attributes_lod = self.db_table.attributes
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod='')



class ui_table(Portlets.Table):
    definition = \
    [
        {'column_name': 'id',               'column_number':  0, 'visible': False},
        {'column_name': 'user_group',       'column_number':  1, 'column_label': 'Benutzergruppe'},
        {'column_name': 'description',      'column_number':  2, 'column_label': 'Beschreibung'},
        {'column_name': 'password',         'column_number':  3, 'visible': False}
    ]

    def __init__(self, db_object, form_object):
        self.db_object = db_object
        self.db_table = db_table(self.db_object)

        Portlets.Table.__init__(self, form_object)
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition)

        #self.add_filter(filter_name='<alle>', filter_function=self.db_table.get_all)
        #self.add_filter(filter_name=None)
        #self.set_filter(filter_name='<alle>')
        self.Table.set_sort_column('description')






