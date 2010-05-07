# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS aircraft module. Completely rewritten in v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import gtk
import table_portlet
import report_exporter

from BaseUI import Portlets
from BaseUI.DB import SQLdb
from BaseUI.GTK import Transformations as GTK_Transformations, DataViews

from charge import db_table_charge
from person import db_table_person
from flight_types import db_table_flight_types
from config import *

DEBUG = False

if DEBUG:
    from pprint import pprint


class main:
    def __init__(self, db_object=None):
        self.db_object = db_object
        self.db_table = db_table_aircraft(self.db_object)

        self.ui_form = ui_form(self.db_object)
        self.ui_table = ui_table(self.db_object, self.ui_form)

        self.portlet = self.ui_table.portlet
        self.toolbar = self.ui_table.toolbar


    def update(self):
        self.ui_table.update()



class aircraft:
    def __init__(self, db_object, id):
        self.db_table = db_table(db_object)

        self.pilot = None
        self.companion = None

        self.location = None
        self.starting_time = None
        self.landing_time = None


    # Starting and landing stuff ----------------------------------------------
    def start(self, timestamp, location, pilot, companion, type=None):
        ''' type = 'self' for selfstart,
                   'tow' for towstart,
                   'winch' for winchstart. '''

        self.starting_time = timestamp
        self.location = location

        self.pilot = pilot
        self.companion = companion


    def land(self, timestamp, location, type=None):
        self.landing_time = timestamp
        self.location = location


    def touch_and_go(self, timestamp):
        self.land(timestamp, self.location)
        self.start(timestamp, self.location, self.pilot, self.companion)


    def add_towed_plane(self, aircraft_obj):
        self.towed_aircraft = aircraft_obj



class db_table_aircraft(SQLdb.table):
    attributes = \
    [
        {'column_name': 'id',                 'data_type': 'bigint' , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'fk_aircraft_charge', 'data_type': 'bigint',  'referenced_table_name': 'charge', 'referenced_column_name': 'id'},
        {'column_name': 'fk_aircraft_owner',  'data_type': 'bigint',  'referenced_table_name': 'person', 'referenced_column_name': 'id'},
        {'column_name': 'country_code',       'data_type': 'varchar', 'character_maximum_length': 10},
        {'column_name': 'aircraft_id',        'data_type': 'varchar', 'character_maximum_length': 10},
        {'column_name': 'aircraft_pattern',   'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'aircraft_seats',     'data_type': 'integer'},
        {'column_name': 'runtime_counter',    'data_type': 'bool'},
        {'column_name': 'tow_plane' ,         'data_type': 'bool'},
        {'column_name': 'center_tow_clutch',  'data_type': 'bool'},
        {'column_name': 'bow_tow_clutch',     'data_type': 'bool'},
        {'column_name': 'self_start',         'data_type': 'bool'},
        {'column_name': 'airborne',           'data_type': 'bool'},
        {'column_name': 'created',            'data_type': 'timestamp'},
        {'column_name': 'updated',            'data_type': 'timestamp'},
        {'column_name': 'deactivated',        'data_type': 'bool'},
    ]


    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'aircraft')
        self.check_attributes(self.attributes, add=True)
        
        self.db_table_flight_types = db_table_flight_types(db_object)
        self.db_table_flight_types_link = db_table_flight_types_link(db_object)
        

    def get_all(self):
        pass


    def get_aircraft_on_ground(self):
        aircraft_lod = self.select(column_list=['*'], where="airborne <> '1'")
        return aircraft_lod
        
    
    def get_airbourne_aircraft(self):
        aircraft_lod = self.select(column_list=['*'], where="airbourne = '1'")
        return aircraft_lod
    
    
    def get_allowed_flight_types(self, id):
        flight_types_lod = self.db_table_flight_types.select() 
        allowed_flight_types_lod = self.db_table_flight_types_link.select(where='fk_aircraft_id = %s' % id)

        for allowed_flight_type_dic in allowed_flight_types_lod:
            for flight_type_dic in flight_types_lod:    
                if allowed_flight_type_dic['fk_flight_type_id'] == flight_type_dic['id']: 
                    allowed_flight_type_dic.update(flight_type_dic)
        return allowed_flight_types_lod
    
    
    
class ui_form(Portlets.Form):
    def __init__(self, db_object):
        self.definition = \
        [
            {'column_name': 'fk_aircraft_charge', 'widget_name': 'comboboxentry_charge_name'    , 'column_number':  5, 'column_label': 'Gebührensatz', 
                            'populate_from': ['charge_name'], 'mask': '%(charge_name)s'}, 
            {'column_name': 'fk_aircraft_owner',  'widget_name': 'comboboxentry_aircraft_owner' , 'column_number': 10, 'column_label': 'Halter',       
                            'populate_from': ['lastname', 'firstname'], 'mask': '%(lastname)s, %(firstname)s'}, 
            {'column_name': 'country_code',       'widget_name': 'entry_country_code'           , 'column_number':  2, 'column_label': 'Land'},
            {'column_name': 'aircraft_id',        'widget_name': 'entry_aircraft_id'            , 'column_number':  1, 'column_label': 'Kennzeichen'},
            {'column_name': 'aircraft_pattern',   'widget_name': 'entry_aircraft_pattern'       , 'column_number':  4, 'column_label': 'Muster'},
            {'column_name': 'aircraft_seats',     'widget_name': 'entry_aircraft_seats'         , 'column_number':  6, 'column_label': 'Sitzplätze'},
            {'column_name': 'runtime_counter',    'widget_name': 'checkbutton_runtime_counter'  , 'column_number':  7, 'column_label': 'Laufzeitzähler'},
            {'column_name': 'tow_plane',          'widget_name': 'checkbutton_tow_plane'        , 'column_number':  8, 'column_label': 'Schleppfähig'},
            {'column_name': 'center_tow_clutch',  'widget_name': 'checkbutton_center_tow_clutch', 'column_number':  9, 'column_label': 'Schwepunktkupplung'},
            {'column_name': 'bow_tow_clutch',     'widget_name': 'checkbutton_bow_tow_clutch'   , 'column_number': 11, 'column_label': 'Bugkupplung'},
            {'column_name': 'self_start',         'widget_name': 'checkbutton_self_start'       , 'column_number': 12, 'column_label': 'Eigenstartfähig'},
            {'column_name': 'airborne',           'widget_name': 'checkbutton_airborne'         , 'column_number': 13, 'column_label': 'In der Luft'},
            {'column_name': 'created',            'widget_name': None                           , 'column_number': 15, 'visible': False},
            {'column_name': 'updated',            'widget_name': None                           , 'column_number': 15, 'visible': False},
            {'column_name': 'deactivated',        'widget_name': 'checkbutton_deactivated'      , 'column_number': 14, 'visible': False}
        ]        
        
        self.db_object = db_object
        self.db_table_aircraft = db_table_aircraft(self.db_object)
        self.db_table_charge = db_table_charge(self.db_object)
        self.db_table_person = db_table_person(self.db_object)
        self.db_table_flight_types_link = db_table_flight_types_link(self.db_object)
        
        self.ui_table_allowed_flight_types = ui_table_allowed_flight_types(self.db_object, self)
        self.portlets = \
        [
            {'portlet': self.ui_table_allowed_flight_types.portlet, 
             'container': 'scrolledwindow_flight_types',
             'save_function': self.ui_table_allowed_flight_types.save_dataset,
             'populate_function': self.ui_table_allowed_flight_types.populate,
             'delete_function': self.db_table_flight_types_link.delete_aircraft},
        ]
        
        Portlets.Form.__init__(self, icon_file=RESOURCE_DIR + 'aircraft_32.png', title='Flugzeuge', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_aircraft', help_file='user/aircraft.html')
        self.attributes_lod = self.db_table_aircraft.attributes
        self.initialize(db_table_object=self.db_table_aircraft,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod=self.portlets)
        
        
        
class ui_table(Portlets.Table):
    def __init__(self, db_object, form_object):
        self.definition = \
        [
            {'column_name': 'id',                  'column_number':  0, 'visible': False},
            {'column_name': 'fk_aircraft_charge',  'column_number':  4, 'column_label': 'Gebührensatz',
                            'populate_from': ['charge_name'],           'mask': '%(charge_name)s'},
            {'column_name': 'fk_aircraft_owner',   'column_number': 11, 'column_label': 'Halter',
                            'populate_from': ['lastname', 'firstname'], 'mask': '%(lastname)s, %(firstname)s'}, 
            {'column_name': 'country_code',        'column_number':  2, 'column_label': 'Land'},
            {'column_name': 'aircraft_id',         'column_number':  1, 'column_label': 'Kennzeichen'},
            {'column_name': 'aircraft_pattern',    'column_number':  3, 'column_label': 'Muster'},
            {'column_name': 'aircraft_seats',      'column_number':  5, 'column_label': 'Sitzplätze'},
            {'column_name': 'runtime_counter',     'column_number':  6, 'column_label': 'Laufzeitzähler'},
            {'column_name': 'tow_plane',           'column_number':  7, 'column_label': 'Schleppfähig'},
            {'column_name': 'center_tow_clutch',   'column_number':  8, 'column_label': 'Schwepunktkupplung'},
            {'column_name': 'bow_tow_clutch',      'column_number':  9, 'column_label': 'Bugkupplung'},
            {'column_name': 'self_start',          'column_number': 10, 'column_label': 'Eigenstartfähig'},
            {'column_name': 'airborne',            'column_number': 12, 'column_label': 'In der Luft'},
            {'column_name': 'created',             'column_number': 13, 'visible': False},
            {'column_name': 'updated',             'column_number': 14, 'visible': False},
            {'column_name': 'deactivated',         'column_number': 15, 'visible': False}
        ]
            
        self.db_object = db_object
        self.db_table_aircraft = db_table_aircraft(self.db_object)

        Portlets.Table.__init__(self, form_object)
        self.initialize(db_table_object=self.db_table_aircraft,
                        definition_lod=self.definition)

        self.add_filter(filter_name='<alle>', filter_function=self.db_table.get_all)
        self.add_filter(filter_name=None)
        self.set_filter(filter_name='<alle>')
        self.Table.set_sort_column('aircraft_id')
        
        

class db_table_flight_types_link(SQLdb.table):
    attributes = \
    [
        {'column_name': 'fk_aircraft_id',     'data_type': 'bigint',  'referenced_table_name': 'aircraft',     'referenced_column_name': 'id'},
        {'column_name': 'fk_flight_type_id',  'data_type': 'bigint',  'referenced_table_name': 'flight_types', 'referenced_column_name': 'id'},
    ]    
    
    
    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'flight_types_link')
        self.check_attributes(self.attributes, add=True)
        
        
    def set_allowed_flight_types(self, aircraft_id, flight_type_id_list):
        #self.delete(column='fk_aircraft_id', value=aircraft_id)
        
        #for content_dic in content_lod:
        #    self.insert('fk_aircraft_id': content_dic['id'], 'fk_flight_type_id': None)
        return
        
        
    def get_allowed_flight_types(self, aircraft_id):
        allowed_flight_types_lod = self.select(where='fk_aircraft_id = %s' % aircraft_id)
        return allowed_flight_types_lod    
        
    
    def delete_aircraft(self, id):
        self.delete('fk_aircraft_id', id)
        
        
        
class ui_table_allowed_flight_types(DataViews.Tree):
    def __init__(self, db_object, parent_form):
        self.definition = \
        [
            {'column_name': 'id',          'column_number': 0, 'visible': False,               'data_type': 'bigint'},
            {'column_name': 'abbrevation', 'column_number': 1, 'column_label': 'Kürzel',       'data_type': 'varchar'},
            {'column_name': 'description', 'column_number': 2, 'column_label': 'Beschreibung', 'data_type': 'varchar'},
            {'column_name': 'allowed',     'column_number': 3, 'column_label': 'Erlaubt?',     'data_type': 'boolean', 'editable': True},
        ]
        
        self.parent_form = parent_form
        
        self.db_object = db_object
        self.db_table_flight_types_link = db_table_flight_types_link(self.db_object)
        self.db_table_flight_types = db_table_flight_types(self.db_object)
        
        self.tree = DataViews.Tree()
        self.tree.create()
        self.portlet = self.tree.widget
        
        self.tree.initialize(self.definition)
        

    def populate(self):
        aircraft_pk = self.parent_form.primary_key
        content_lod = self.db_table_flight_types.select() 
        allowed_flight_types_lod = self.db_table_flight_types_link.select(where='fk_aircraft_id = %s' % aircraft_pk)
        if DEBUG: print 'allowed_flight_types_lod:'; pprint(allowed_flight_types_lod)  
         
        for content_dic in content_lod:
            for allowed_flight_type_dic in allowed_flight_types_lod:
                if allowed_flight_type_dic['fk_flight_type_id'] == content_dic['id']: 
                    content_dic['allowed'] = True
                    
        if DEBUG: print 'content_lod:'; pprint(content_lod)        
        self.tree.populate(content_lod)
                
        
    def save_dataset(self, aircraft_pk):
        self.db_table_flight_types_link.delete('fk_aircraft_id', aircraft_pk)
        
        tree_content_lod = self.tree.get_content()
        for content_dic in tree_content_lod:
            if content_dic['allowed'] == True:
                self.db_table_flight_types_link.insert(content={'fk_aircraft_id': aircraft_pk, 'fk_flight_type_id': content_dic['id']})
        
        
        