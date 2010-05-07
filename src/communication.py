# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS communication module. Introduced in v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

from BaseUI import Portlets
from BaseUI.DB import SQLdb
from config import *


class main:
    def __init__(self, db_object=None, parent_form=None):
        self.db_object = db_object
        self.db_table = db_table(self.db_object)
        
        self.ui_form = ui_form(self.db_object, parent_form)
        self.ui_table = ui_table(self.db_object, self.ui_form, parent_form)

        self.portlet = self.ui_table.portlet
    
    

class communication:
    def __init__(self):
        pass
    
    
    
class db_table(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',          'data_type': 'bigint',  'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'fk_person',   'data_type': 'bigint',  'referenced_table_name': 'person', 'referenced_column_name': 'id'},
        {'column_name': 'fk_club',     'data_type': 'bigint',  'referenced_table_name': 'clubs',  'referenced_column_name': 'id'},
        {'column_name': 'description', 'data_type': 'varchar', 'character_maximum_length': 40}, # f.e. 'Bussiness' or 'Private'
        {'column_name': 'type',        'data_type': 'varchar', 'character_maximum_length': 40},        # f.e. 'Phone', 'Mobile' or 'eMail'
        {'column_name': 'address',     'data_type': 'varchar', 'character_maximum_length': 40},       # f.e. 'john.doe@foobar.org'
        {'column_name': 'created',     'data_type': 'timestamp'},
        {'column_name': 'updated',     'data_type': 'timestamp'},
        {'column_name': 'deactivated', 'data_type': 'bool'}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'communication')
        self.check_attributes(self.attributes, add=True)
        
    
    def delete_person(self, id):
        self.delete('fk_person', id)
        
        
    def delete_club(self, id):
        self.delete_('fk_club', id)



class ui_form(Portlets.Form):
    def __init__(self, db_object, parent_form=None):
        self.definition = \
        [
            {'column_name': 'description', 'widget_name': 'entry_description'},
            {'column_name': 'type',        'widget_name': 'comboboxentry_type', 'populate_function': self.populate_type},
            {'column_name': 'address',     'widget_name': 'entry_address'}
        ]
    
        Portlets.Form.__init__(self, parent_form, icon_file=RESOURCE_DIR + 'person_16.png', title='Kommunikation', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_communication', help_file='user/person.html')
        
        self.db_object = db_object
        self.db_table = db_table(self.db_object)

        self.attributes_lod = self.db_table.attributes
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod)
        
        
    def populate_type(self, widget, foreign_content_dic=None):
        content_lod = self.db_table.select(distinct=True, column_list=['type'])
        widget.initialize({'column_name': 'type'})
        widget.populate(content_lod)
        
        
        
class ui_table(Portlets.Table):
    definition = \
    [
        {'column_name': 'id',          'column_number':  0, 'visible': False},
        {'column_name': 'type',        'column_number':  1, 'column_label': 'Typ'},
        {'column_name': 'description', 'column_number':  2, 'column_label': 'Beschreibung'},
        {'column_name': 'address',     'column_number':  3, 'column_label': 'Adresse/Nummer'},
    ]
    
    def __init__(self, db_object, form_object, parent_form=None):
        Portlets.Table.__init__(self, form_object, parent_form, filter=False, help=False, separate_toolbar=False)
        
        self.db_object = db_object
        self.db_table = db_table(self.db_object)

        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition)

        self.Table.set_sort_column('type')
        
        
        
class db_table_communication_link:
    # TODO: This is needed to patch companys, persons, clubs and other together!
    def __init__(self):
        pass
    
    
        