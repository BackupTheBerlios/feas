# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS person module. Introduced in v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import address
import communication

from BaseUI import Portlets
from BaseUI.DB import SQLdb
from config import RESOURCE_DIR


class main:
    def __init__(self, db_object=None):
        self.db_object = db_object
        self.db_table_person = db_table_person(self.db_object)

        self.ui_form = ui_form(self.db_object)
        self.ui_table = ui_table(self.db_object, self.ui_form)

        self.portlet = self.ui_table.portlet
        self.toolbar = self.ui_table.toolbar


    def update(self):
        self.ui_table.update()



class person:
    def __init__(self, id=None):
        pass


    def set_airbourne(self, aircraft_id):
        pass


    def set_grounded(self):
        pass
    
    
    def add_address(self):
        pass
    
    
    def remove_address(self):
        pass



class db_table_person(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',                        'data_type': 'bigint' , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'fk_airbourne',              'data_type': 'bigint',  'referenced_table_name': 'aircraft'},
        {'column_name': 'fk_standard_communication', 'data_type': 'bigint',  'referenced_table_name': 'communication'},
        {'column_name': 'fk_standard_address',       'data_type': 'bigint',  'referenced_table_name': 'address'},
        {'column_name': 'fk_standard_company',       'data_type': 'bigint',  'referenced_table_name': 'company'},
        {'column_name': 'salutation',                'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'title',                     'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'firstname',                 'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'lastname',                  'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'birthday',                  'data_type': 'date'},
        {'column_name': 'password',                  'data_type': 'varchar', 'character_maximum_length': 128},
        {'column_name': 'created',                   'data_type': 'timestamp'},
        {'column_name': 'updated',                   'data_type': 'timestamp'},
        {'column_name': 'deactivated',               'data_type': 'bool'},
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'person')
        differences_lod = self.check_attributes(self.attributes, add=True)
        #self.db_table_person_person_link = db_table_person_person_link(db_object)


    def get_login_lod(self):
        sql_command = '''\
SELECT  id, firstname, lastname, user_group.password
FROM    person LEFT OUTER JOIN user_group ON fk_user_group = user_group.id
WHERE   deactivated IS NULL'''
        result = self.db_object.dictresult(sql_command)
        return result


    def get_all(self):
        print "get 'em all!"



class ui_form(Portlets.Form):
    def __init__(self, db_object):
        Portlets.Form.__init__(self, icon_file=RESOURCE_DIR + 'person_16.png', title='Personen', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_person', help_file='user/person.html')
        
        self.definition = \
        [
            {'column_name': 'salutation', 'widget_name': 'comboboxentry_salutation', 'populate_function': self.populate_salutation},
            {'column_name': 'title',      'widget_name': 'comboboxentry_title',      'populate_function': self.populate_title},
            {'column_name': 'firstname',  'widget_name': 'entry_firstname'},
            {'column_name': 'lastname',   'widget_name': 'entry_lastname'},
            {'column_name': 'birthday',   'widget_name': 'entry_birthday'},
            {'column_name': 'password',   'widget_name': 'entry_password'},
        ]
        
        self.db_object = db_object
        self.db_table_person = db_table_person(self.db_object)
        
        self.address_main = address.main(self.db_object, parent_form=self)
        self.communication_main = communication.main(self.db_object, parent_form=self)
        
        self.portlets = \
        [
            {'portlet': self.address_main.portlet, 
             'container': 'alignment_address',
             'populate_function': self.address_main.ui_table.populate,
             'delete_function': self.address_main.db_table.delete_person},
            {'portlet': self.communication_main.portlet, 
             'container': 'alignment_communication',
             'populate_function': self.communication_main.ui_table.populate,
             'delete_function': self.communication_main.db_table.delete_person},
        ]
        
        self.attributes_lod = self.db_table_person.attributes
        self.initialize(db_table_object=self.db_table_person,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod=self.portlets)
        
        
    def populate_salutation(self, widget, foreign_content_dic=None):
        content_lod = self.db_table_person.select(distinct=True, 
                                                  column_list=['salutation'])
        widget.initialize({'column_name': 'salutation'})
        widget.populate(content_lod)
        
        
    def populate_title(self, widget, foreign_content_dic=None):
        content_lod = self.db_table_person.select(distinct=True, 
                                           column_list=['title'])
        widget.initialize({'column_name': 'title'})
        widget.populate(content_lod)
        


class ui_table(Portlets.Table):
    definition = \
    [
        {'column_name': 'id',                        'column_number':  0, 'visible': False},
        {'column_name': 'salutation',                'column_number':  1, 'column_label': 'Anrede'},
        {'column_name': 'title',                     'column_number':  2, 'column_label': 'Titel'},
        {'column_name': 'lastname',                  'column_number':  3, 'column_label': 'Nachname'},
        {'column_name': 'firstname',                 'column_number':  4, 'column_label': 'Vorname'},
        {'column_name': 'fk_standard_communication', 'column_number':  5, 'column_label': 'Kommunikation'},
        {'column_name': 'fk_standard_address',       'column_number':  6, 'column_label': 'Adresse'},
        {'column_name': 'fk_standard_company',       'column_number':  7, 'column_label': 'Firma'},
        {'column_name': 'birthday',                  'column_number':  8, 'column_label': 'Geburtsdatum'},
        {'column_name': 'deactivated',               'column_number':  9, 'column_label': 'Deaktiviert?', 'visible': False}
    ]

    def __init__(self, db_object, form_object):
        self.db_object = db_object
        self.db_table_person = db_table_person(self.db_object)

        Portlets.Table.__init__(self, form_object)
        self.initialize(db_table_object=self.db_table_person,
                        definition_lod=self.definition)

        self.add_filter(filter_name='<alle>', filter_function=self.db_table_person.get_all)
        self.add_filter(filter_name=None)
        self.set_filter(filter_name='<alle>')
        self.Table.set_sort_column('lastname')



# Person link -----------------------------------------------------------------
#class db_table_person_person_link(SQLdb.table):
#    attributes =  \
#    [
#        {'column_name': 'fk_person',        'data_type': 'bigint', 'referenced_table_name': 'person',        'referenced_column_name': 'id'},
#        {'column_name': 'fk_company',       'data_type': 'bigint', 'referenced_table_name': 'company',       'referenced_column_name': 'id'},
#        {'column_name': 'fk_address',       'data_type': 'bigint', 'referenced_table_name': 'address',       'referenced_column_name': 'id'},
#        {'column_name': 'fk_communication', 'data_type': 'bigint', 'referenced_table_name': 'communication', 'referenced_column_name': 'id'},
#    ]

#    def __init__(self, db_object):
#        SQLdb.table.__init__(self, db_object, 'person_link')
#        differences_lod = self.check_attributes(self.attributes, action='add')




