# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS address module. Introduced in v0.8 alpha.
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
    
    
    
class address:
    def __init__(self, db_object):
        self.db_table = db_table(db_object)
        
        
    def add(self):
        print "add address"
        
        
    def remove(self):
        print "remove adress"
        
        
    def set_default(self):
        print "set default address"
        
        
    def get_by_person(self, user_id):
        pass
    
    
    def get_by_company(self, company_id):
        pass
        
        
        
class db_table(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',           'data_type': 'bigint',  'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'fk_person',    'data_type': 'bigint', 'referenced_table_name': 'person', 'referenced_column_name': 'id'},
        {'column_name': 'fk_club',      'data_type': 'bigint', 'referenced_table_name': 'clubs',  'referenced_column_name': 'id'},
        {'column_name': 'type',         'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'country_code', 'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'country',      'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'post_code',    'data_type': 'varchar', 'character_maximum_length': 10},
        {'column_name': 'city',         'data_type': 'varchar', 'character_maximum_length': 40}, 
        {'column_name': 'street',       'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'house_number', 'data_type': 'varchar', 'character_maximum_length': 10},
        {'column_name': 'created',      'data_type': 'timestamp'},
        {'column_name': 'updated',      'data_type': 'timestamp'},
        {'column_name': 'deactivated',  'data_type': 'bool'}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'address')
        self.check_attributes(self.attributes, add=True)


    def delete_person(self, id):
        self.delete('fk_person', id)
        
        
    def delete_club(self, id):
        self.delete('fk_club', id)
        
        
#    def select_by_person(self, person_id):
#        sql_command = """\
#SELECT * FROM address LEFT OUTER JOIN person ON fk_person = person.id """
#        return self.db_object.dictresult(sql_command) 
    
    
#    def select_by_company(self, company_id):
#        pass
    
        
        
class ui_form(Portlets.Form):
    def __init__(self, db_object, parent_form=None):
        self.definition = \
        [
            {'column_name': 'type'        , 'widget_name': 'comboboxentry_type',         'populate_function': self.populate_type},
            {'column_name': 'country_code', 'widget_name': 'comboboxentry_country_code', 'populate_function': self.populate_country_code},
            {'column_name': 'country'     , 'widget_name': 'comboboxentry_country',      'populate_function': self.populate_country},
            {'column_name': 'post_code'   , 'widget_name': 'comboboxentry_post_code',    'populate_function': self.populate_post_code},
            {'column_name': 'city'        , 'widget_name': 'comboboxentry_city',         'populate_function': self.populate_city},
            {'column_name': 'street'      , 'widget_name': 'comboboxentry_street',       'populate_function': self.populate_street},
            {'column_name': 'house_number', 'widget_name': 'entry_house_number'}
        ]
        
        Portlets.Form.__init__(self, parent_form, icon_file=RESOURCE_DIR + 'person_16.png', title='Adresse', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_address', help_file='user/person.html')
        
        self.db_object = db_object
        self.db_table = db_table(self.db_object)

        self.attributes_lod = self.db_table.attributes
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod)
        
        
    def populate_type(self, widget, foreign_content_dic=None):
        content_lod = self.db_table.select(distinct=True, 
                                           column_list=['type'])
        widget.initialize({'column_name': 'type'})
        widget.populate(content_lod)
        
        
    def populate_country_code(self, widget, foreign_content_dic=None):
        content_lod = self.db_table.select(distinct=True, 
                                           column_list=['country_code'])
        widget.initialize({'column_name': 'country_code'})
        widget.populate(content_lod)
        
        
    def populate_country(self, widget, foreign_content_dic=None):
        content_lod = self.db_table.select(distinct=True, 
                                           column_list=['country'])
        widget.initialize({'column_name': 'country'})
        widget.populate(content_lod)
        
                
    def populate_post_code(self, widget, foreign_content_dic=None):
        content_lod = self.db_table.select(distinct=True, 
                                           column_list=['post_code'])
        widget.initialize({'column_name': 'post_code'})
        widget.populate(content_lod)
        
        
    def populate_city(self, widget, foreign_content_dic=None):
        content_lod = self.db_table.select(distinct=True, 
                                           column_list=['city'])
        widget.initialize({'column_name': 'city'})
        widget.populate(content_lod)


    def populate_street(self, widget, foreign_content_dic=None):
        content_lod = self.db_table.select(distinct=True, 
                                           column_list=['street'])
        widget.initialize({'column_name': 'street'})
        widget.populate(content_lod)
                        


class ui_table(Portlets.Table):
    definition = \
    [
        {'column_name': 'id'          , 'column_number':  0, 'visible': False},
        {'column_name': 'type'        , 'column_number':  1, 'column_label': 'Typ'},
        {'column_name': 'country_code', 'column_number':  2, 'column_label': 'Ländercode', 'visible': False},
        {'column_name': 'post_code'   , 'column_number':  3, 'column_label': 'PLZ'},
        {'column_name': 'city'        , 'column_number':  4, 'column_label': 'Stadt'},
        {'column_name': 'street'      , 'column_number':  5, 'column_label': 'Straße'},
        {'column_name': 'standart'    , 'column_number':  6, 'column_label': 'Standart', 'data_type': 'bool', 'editable': True},
    ]
    
    def __init__(self, db_object, form_object, parent_form=None):
        Portlets.Table.__init__(self, form_object, parent_form, filter=False, help=False, separate_toolbar=False)
        
        self.db_object = db_object
        self.db_table = db_table(self.db_object)
        
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition)

        self.Table.set_sort_column('type')
        
        
        
        
        