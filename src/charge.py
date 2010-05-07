# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS charge module. Recoded in v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

from BaseUI import Portlets
from BaseUI.DB import SQLdb
from BaseUI.GTK import DataViews
from config import *


class main:
    def __init__(self, db_object=None):
        self.db_object = db_object
        self.db_table_charge = db_table_charge(self.db_object)
        self.db_table_start_charge = db_table_start_charge(self.db_object)
        self.db_table_landing_charge = db_table_landing_charge(self.db_object)
        self.db_charge_template = db_table_charge_template(self.db_object)

        self.ui_form = ui_form(self.db_object)
        self.ui_table = ui_table(self.db_object, self.ui_form)

        self.portlet = self.ui_table.portlet
        self.toolbar = self.ui_table.toolbar


    def update(self):
        self.ui_table.update()
   # def get_portlet(self):
   #     return self.portlet


   # def get_toolbar(self):
   #     return self.toolbar



class charge:
    def __init__(self, db_object, id):
        self.db_table = db_table(db_object)


    def dummy(self):
        pass



class db_table_charge(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',               'data_type': 'bigint' , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'charge_name',      'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'created',          'data_type': 'timestamp'},
        {'column_name': 'updated',          'data_type': 'timestamp'},
        {'column_name': 'deactivated',      'data_type': 'bool'}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'charge')
        self.check_attributes(self.attributes, add=True)
        

    def get_all(self):
        pass



class ui_form(Portlets.Form):
    def __init__(self, db_object):
        self.definition = \
        [
            {'column_name': 'charge_name',  'widget_name': 'entry_charge_name'}
        ]
        
        self.db_object = db_object
        self.db_table_charge = db_table_charge(self.db_object)

        # Portlets -------------------------------------------------------------
        self.ui_table_start_charge = ui_table_start_charge(self.db_object, self)
        self.ui_table_landing_charge = ui_table_landing_charge(self.db_object, self)
        self.ui_form_charge_template = ui_form_charge_template(self.db_object)
        self.ui_table_charge_templates = ui_table_charge_templates(self.db_object, self.ui_form_charge_template)
        self.portlets = \
        [
            {
                'portlet': self.ui_table_start_charge.portlet,
                'container': 'scrolledwindow_start_charges',
                'save_function': self.ui_table_start_charge.save_dataset,
                'populate_function': self.ui_table_start_charge.populate
            },
            {
                'portlet': self.ui_table_landing_charge.portlet,
                'container': 'scrolledwindow_landing_charges',
                'save_function': self.ui_table_landing_charge.save_dataset,
                'populate_function': self.ui_table_landing_charge.populate
            },
            {
                'portlet': self.ui_table_charge_templates.portlet,
                'container': 'eventbox_charge_templates',
            },
        ]
        
        Portlets.Form.__init__(self, icon_file=RESOURCE_DIR + 'euro_32.png', title='Gebühren', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_charge', help_file='user/charge.html')
        self.attributes_lod = self.db_table_charge.attributes
        self.initialize(db_table_object=self.db_table_charge,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod=self.portlets)

        

class ui_table(Portlets.Table):
    definition = \
    [
        {'column_name': 'id',               'column_number':  0, 'visible': False},
        {'column_name': 'charge_name',      'column_number':  1, 'column_label': 'Bezeichnung'},
    ]

    def __init__(self, db_object, form_object):
        self.db_object = db_object
        self.db_table_charge = db_table_charge(self.db_object)

        Portlets.Table.__init__(self, form_object)
        self.initialize(db_table_object=self.db_table_charge,
                        definition_lod=self.definition)

        self.add_filter(filter_name='<alle>', filter_function=self.db_table.get_all)
        self.add_filter(filter_name=None)
        self.set_filter(filter_name='<alle>')
        self.Table.set_sort_column('charge_name')



# Start charge definition -----------------------------------------------------
class db_table_start_charge(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'fk_charge',         'data_type': 'bigint',  'referenced_table_name': 'address',        'referenced_column_name': 'id'},
        {'column_name': 'fk_flight_type',    'data_type': 'bigint',  'referenced_table_name': 'address',        'referenced_column_name': 'id'},

        {'column_name': 'fk_start_type'     , 'data_type': 'bigint',  'referenced_table_name': 'start_type',      'referenced_column_name': 'id'},
        {'column_name': 'fk_charge_template', 'data_type': 'bigint',  'referenced_table_name': 'charge_template', 'referenced_column_name': 'id'},
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'start_charge')
        differences_lod = self.check_attributes(self.attributes, add=True)



class ui_table_start_charge(DataViews.Tree):
    def __init__(self, db_object, parent_form):
        self.definition = \
        [
            {'column_name': 'id',                        'column_number': 0, 'visible': False,                'data_type': 'bigint'},
            {'column_name': 'abbrevation',               'column_number': 1, 'column_label': 'Kürzel',        'data_type': 'varchar'},
            {'column_name': 'description',               'column_number': 2, 'column_label': 'Beschreibung',  'data_type': 'varchar'},
            {'column_name': 'fk_start_charge_self',      'column_number': 3, 'column_label': 'Eigenstart',    'data_type': '#combobox', 'editable': True},
            {'column_name': 'fk_start_charge_winch',     'column_number': 4, 'column_label': 'Windenstart',   'data_type': '#combobox', 'editable': True},
            {'column_name': 'fk_start_charge_tow',       'column_number': 5, 'column_label': 'F-Schlepp',     'data_type': '#combobox', 'editable': True},
            {'column_name': 'fk_start_charge_doubletow', 'column_number': 6, 'column_label': 'Doppelschlepp', 'data_type': '#combobox', 'editable': True, 'visible': False},
        ]
        
        self.parent_form = parent_form
        
        self.db_object = db_object
        #self.db_table_flight_types_link = db_table_flight_types_link(self.db_object)
        #self.db_table_flight_types = db_table_flight_types(self.db_object)
        
        self.tree = DataViews.Tree()
        self.tree.create()
        self.portlet = self.tree.widget
        
        self.tree.initialize(self.definition)
        

    def populate(self):
        #aircraft_pk = self.parent_form.primary_key
        #content_lod = self.db_table_flight_types.select() 
        #allowed_flight_types_lod = self.db_table_flight_types_link.select(where='fk_aircraft_id = %s' % aircraft_pk)
         
        #for content_dic in content_lod:
        #    for allowed_flight_type_dic in allowed_flight_types_lod:
        #        if allowed_flight_type_dic['fk_flight_type_id'] == content_dic['id']: 
        #            content_dic['allowed'] = True
        for definition_dict in self.definition:
            if definition_dict.has_key('#liststore'):
                definition_dict['#liststore'].clear()
                definition_dict['#liststore'].append([0, '-'])
                
        print 'populating start_charges'
        self.tree.populate([{'id': 1, 'abbrevation': 'S'}])
            
        
    def save_dataset(self, charge_pk):
        #self.db_table_flight_types_link.delete('fk_aircraft_id', aircraft_pk)
        
        #tree_content_lod = self.tree.get_content()
        #for content_dic in tree_content_lod:
        #    if content_dic['allowed'] == True:
        #        self.db_table_flight_types_link.insert(content={'fk_aircraft_id': aircraft_pk, 'fk_flight_type_id': content_dic['id']})
        print 'saving start_charges'
        
        
        
class ui_table_landing_charge(DataViews.Tree):
    def __init__(self, db_object, parent_form):
        self.definition = \
        [
            {'column_name': 'id',                          'column_number': 0, 'visible': False,                'data_type': 'bigint'},
            {'column_name': 'abbrevation',                 'column_number': 1, 'column_label': 'Kürzel',        'data_type': 'varchar'},
            {'column_name': 'description',                 'column_number': 2, 'column_label': 'Beschreibung',  'data_type': 'varchar'},
            {'column_name': 'fk_landing_charge_self',      'column_number': 3, 'column_label': 'Eigenstart',    'data_type': '#combobox', 'editable': True},
            {'column_name': 'fk_landing_charge_winch',     'column_number': 4, 'column_label': 'Windenstart',   'data_type': '#combobox', 'editable': True},
            {'column_name': 'fk_landing_charge_tow',       'column_number': 5, 'column_label': 'F-Schlepp',     'data_type': '#combobox', 'editable': True},
            {'column_name': 'fk_landing_charge_doubletow', 'column_number': 6, 'column_label': 'Doppelschlepp', 'data_type': '#combobox', 'editable': True, 'visible': False},
        ]
        
        self.parent_form = parent_form
        
        self.db_object = db_object
        #self.db_table_flight_types_link = db_table_flight_types_link(self.db_object)
        #self.db_table_flight_types = db_table_flight_types(self.db_object)
        
        self.tree = DataViews.Tree()
        self.tree.create()
        self.portlet = self.tree.widget
        
        self.tree.initialize(self.definition)
        

    def populate(self):
        #aircraft_pk = self.parent_form.primary_key
        #content_lod = self.db_table_flight_types.select() 
        #allowed_flight_types_lod = self.db_table_flight_types_link.select(where='fk_aircraft_id = %s' % aircraft_pk)
         
        #for content_dic in content_lod:
        #    for allowed_flight_type_dic in allowed_flight_types_lod:
        #        if allowed_flight_type_dic['fk_flight_type_id'] == content_dic['id']: 
        #            content_dic['allowed'] = True
        print 'populating landing_charges'
        self.tree.populate([{'id': 1, 'abbrevation': 'L'}])
            
        
    def save_dataset(self, charge_pk):
        #self.db_table_flight_types_link.delete('fk_aircraft_id', aircraft_pk)
        
        #tree_content_lod = self.tree.get_content()
        #for content_dic in tree_content_lod:
        #    if content_dic['allowed'] == True:
        #        self.db_table_flight_types_link.insert(content={'fk_aircraft_id': aircraft_pk, 'fk_flight_type_id': content_dic['id']})
        print 'saving landing_charges'
    
        

class ui_table_charge_templates(Portlets.Table):
    definition = \
    [
        {'column_name': 'id',   'column_number':  0, 'visible': False},
        {'column_name': 'name', 'column_number':  1, 'column_label': 'Bezeichnung'},
        {'column_name': 'code', 'column_number':  2, 'column_label': 'Quellcode'},
    ]

    def __init__(self, db_object, form_object):
        self.db_object = db_object
        self.db_table_charge_template = db_table_charge_template(self.db_object)

        Portlets.Table.__init__(self, form_object, filter=False, help=False, separate_toolbar=False)
        self.initialize(db_table_object=self.db_table_charge_template,
                        definition_lod=self.definition)

        self.Table.set_sort_column('name')
        


class ui_form_charge_template(Portlets.Form):
    def __init__(self, db_object):
        self.definition = \
        [
            {'column_name': 'name',  'widget_name': 'entry_charge_template_name'},
            {'column_name': 'code',  'widget_name': 'textview_charge_template_code'},
        ]
        
        self.db_object = db_object
        self.db_table_charge_template = db_table_charge_template(self.db_object)
        
        Portlets.Form.__init__(self, icon_file=RESOURCE_DIR + 'euro_32.png', title='Gebührenvorlagen', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_charge_template', help_file='user/charge.html')
        self.attributes_lod = self.db_table_charge_template.attributes
        self.initialize(db_table_object=self.db_table_charge_template,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod=None)
        
        
                
# Landing charge definition ---------------------------------------------------
class db_table_landing_charge(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'fk_charge',         'data_type': 'bigint',  'referenced_table_name': 'address',        'referenced_column_name': 'id'},
        {'column_name': 'fk_flight_type',    'data_type': 'bigint',  'referenced_table_name': 'address',        'referenced_column_name': 'id'},

        {'column_name': 'fk_landing_type'   , 'data_type': 'bigint',  'referenced_table_name': 'start_type',      'referenced_column_name': 'id'},
        {'column_name': 'fk_charge_template', 'data_type': 'bigint',  'referenced_table_name': 'charge_template', 'referenced_column_name': 'id'},
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'landing_charge')
        differences_lod = self.check_attributes(self.attributes, add=True)



# Charge template definition --------------------------------------------------
class db_table_charge_template(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',   'data_type': 'bigint' , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'name', 'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'code', 'data_type': 'text'}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'charge_template')
        differences_lod = self.check_attributes(self.attributes, add=True)



class main_old:
    #db_table_charges_definition = \
    #[
    #    {'db_field_name': 'pk_key_number', 'db_field_type': 'bigint'     , 'gtk_widget_name': 'entry_key_number' , 'gtk_treeview_column': 0, 'print_table_column': 0, 'db_primary_key': True, 'gtk_column_hide': True},
    #    {'db_field_name': 'charge_name'  , 'db_field_type': 'varchar(40)', 'gtk_widget_name': 'entry_charge_name', 'gtk_treeview_column': 1, 'print_table_column': 1, 'column_title': 'Gebührenbezeichnung'},#

    #    {'db_field_name': 'deactivated'       , 'db_field_type': 'bool'        , 'gtk_widget_name': 'checkbutton_deactivated'      , 'gtk_treeview_column': 2, 'print_table_column': 2, 'gtk_column_hide': True},
    #    {'db_field_name': 'last_change_date'  , 'db_field_type': 'date'        , 'gtk_widget_name': None                           , 'gtk_treeview_column': 3, 'print_table_column': 3, 'gtk_column_hide': True}
    #]

#    db_table_start_charges_definition = \
#    [
#        {'db_field_name': 'fk_charge_name'            , 'db_foreign_table': 'charges'         , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_name'            , 'gtk_treeview_column': 0, 'column_title': 'Gebührenbezeichnung'},
#        {'db_field_name': 'fk_flight_type_abbrevation', 'db_foreign_table': 'flight_types'    , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'flight_type_abbrevation', 'gtk_treeview_column': 1, 'column_title': 'Flugart'},

#        {'db_field_name': 'fk_general_charge'         , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 2, 'column_title': 'generell'},
#        {'db_field_name': 'fk_self_start_charge'      , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 3, 'column_title': 'Eigenstart'},
#        {'db_field_name': 'fk_winch_start_charge'     , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 4, 'column_title': 'Windenstart'},
#        {'db_field_name': 'fk_tow_start_charge'       , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 5, 'column_title': 'Schleppstart'}
#    ]

#    db_table_landing_charges_definition = \
#    [
#        {'db_field_name': 'fk_charge_name'            , 'db_foreign_table': 'charges'         , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_name'            , 'gtk_treeview_column': 0, 'column_title': 'Gebührenbezeichnung'},
#        {'db_field_name': 'fk_flight_type_abbrevation', 'db_foreign_table': 'flight_types'    , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'flight_type_abbrevation', 'gtk_treeview_column': 1, 'column_title': 'Flugart'},

#        {'db_field_name': 'fk_general_charge'         , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 2, 'column_title': 'generell'},
#        {'db_field_name': 'fk_self_start_charge'      , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 3, 'column_title': 'Eigenstart'},
#        {'db_field_name': 'fk_winch_start_charge'     , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 4, 'column_title': 'Windenstart'},
#        {'db_field_name': 'fk_tow_start_charge'       , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 5, 'column_title': 'Schleppstart'}
#    ]

#    db_table_charge_templates_definition = \
#    [
#        {'db_field_name': 'pk_key_number'       , 'db_field_type': 'bigint'        , 'gtk_widget_name': 'entry_key_number'             , 'gtk_treeview_column': 0, 'print_table_column': 0, 'db_primary_key': True, 'gtk_column_hide': True},
#        {'db_field_name': 'charge_template_name', 'db_field_type': 'varchar(60)'   , 'gtk_widget_name': 'entry_charge_template_name'   , 'gtk_treeview_column': 1, 'print_table_column': 1, 'column_title': 'Name Gebührenvorlage'},
#        {'db_field_name': 'charge_template_code', 'db_field_type': 'varchar(65536)', 'gtk_widget_name': 'textview_charge_template_code', 'gtk_treeview_column': 2, 'print_table_column': 2, 'column_title': 'Quellcode Vorlage'},

#        {'db_field_name': 'deactivated'       , 'db_field_type': 'bool'        , 'gtk_widget_name': 'checkbutton_deactivated'      , 'gtk_treeview_column': 3, 'print_table_column': 3, 'gtk_column_hide': True},
#        {'db_field_name': 'last_change_date'  , 'db_field_type': 'date'        , 'gtk_widget_name': None                           , 'gtk_treeview_column': 4, 'print_table_column': 4, 'gtk_column_hide': True}
#    ]


    def __init__(self, DBcnx):
        self.db_table_flight_types_charges = db_table(DBcnx, "flight_types_charges")
        self.db_table_flight_types = db_table(DBcnx, "flight_types")
        self.db_table_charges = db_table(DBcnx, "charges")
        self.db_table_charge_templates = db_table(DBcnx, "charge_templates")
        self.db_table_start_charges = db_table(DBcnx, "start_charges")
        self.db_table_landing_charges = db_table(DBcnx, "landing_charges")
        self.liststore_charge_templates = None

        self.form_window = table_portlet.window_form(self.db_table_charges, self.db_table_layout, self.form_portlet_layout())
        self.table_portlet = table_portlet.portlet_table(self.db_table_charges, self.form_window)
        self.class_charge = charge(DBcnx)

    # Widget functions --------------------------------------------------------
    def on_treeview_charges_edited(self, renderer=None, row=None, content=None, model=None, col=None):
        model[row][col] = str(content)

    def on_combocell_edited(self, renderer=None, row=None, content=None, model=None, col=None):
        for row_content in model:
            if content == row_content[1]:
                print row_content[0]

    def on_comboboxentry_simulator_changed(self, widget, data=None):
        start_booking = self.radiobutton_start_booking.get_active()
        landing_booking = self.radiobutton_landing_booking.get_active()
        flight_type = get_comboboxentry_selection(self.comboboxentry_flight_type)
        booking_modality = get_comboboxentry_selection(self.comboboxentry_booking_modality)
        key_number = int(self.form_window.get_widget("entry_key_number").get_text())

        pk_charge_template = self.class_charge.get_charge_template(pk_charge=key_number, booking_modality=booking_modality[0], pk_flight_type=flight_type[0], start=start_booking, landing=landing_booking)
        # This is not right here, give it to on_comboboxentry_changed!
        if pk_charge_template <> None:
            charge_template_name = self.db_table_charge_templates.search_column("pk_key_number", pk_charge_template, "charge_template_name")[0]
            self.comboboxentry_charge_template.child.set_text(unicode(charge_template_name, "latin-1"))
        else:
            self.comboboxentry_charge_template.child.set_text("-")

    def on_simulator_button_refresh_clicked(self, widget=None, data=None):
        try:
            flight_time = float(self.entry_flight_time.get_text())
            motor_runtime= float(self.entry_motor_runtime.get_text())
            tow_altitude= int(self.comboboxentry_tow_altitude.child.get_text())

            # Now, calculate charge
            charge_template_pk = get_comboboxentry_selection(self.comboboxentry_charge_template)[0]
            charge = self.class_charge.calculate_from_template(charge_template_pk, flight_time, motor_runtime, tow_altitude)
            self.entry_charge.set_text(str(charge))
        except Exception, inst:
            dialog(parent=self.window_charges, label_text=str(inst))
        return

    # Main functions ----------------------------------------------------------
    def get_portlet(self):
        portlet = self.table_portlet.initGUIportlet(nowindow=True)
        return portlet

    def get_toolbar(self):
        toolbar = self.table_portlet.get_toolbar()
        return toolbar

    # Widget functions --------------------------------------------------------
    def form_portlet_layout(self):
        portlet_list = []
        portlet_list.append([self.create_treeview_start_charges, "scrolledwindow_start_charges", self.populate_treeview_start_charges, self.save_treeview_start_charges])
        portlet_list.append([self.create_treeview_landing_charges, "scrolledwindow_landing_charges", self.populate_treeview_landing_charges, self.save_treeview_landing_charges])
        portlet_list.append([self.create_treeview_charge_templates, "eventbox_charge_templates", None, None])
        portlet_list.append([self.populate_charge_simulator, None, None, None])
        return portlet_list

    def create_treeview_charge_templates(self, db_charge_table_layout_list):
        form_window_charge_templates = table_portlet.window_form(self.db_table_charge_templates, self.db_layout_dictlist_charge_templates)

        table_portlet_charge_templates = table_portlet.portlet_table(self.db_table_charge_templates, form_window_charge_templates)

        self.portlet_charge_templates = table_portlet_charge_templates.initGUIportlet(nowindow=True, search=False)
        table_portlet_charge_templates.set_update_function(self.update_comboboxes_in_treeview_charges)
        return self.portlet_charge_templates
        #self.alignment_charge_templates.add(self.portlet_charge_templates)

    def create_treeview_start_charges(self, db_table_layout_list):
        self.treeview_start_charges, self.liststore_start_charges = self.create_treeview_charges(self.db_table_start_charges, self.db_table_layout_start_charges())
        return self.treeview_start_charges

    def create_treeview_landing_charges(self, db_table_layout_list):
        self.treeview_landing_charges, self.liststore_landing_charges = self.create_treeview_charges(self.db_table_landing_charges, self.db_table_layout_landing_charges())
        return self.treeview_landing_charges

    def create_treeview_charges(self, db_table, db_table_layout_list):
        treeview_charges = gtk.TreeView()
        table_selection = db_table.verify(db_table_layout_list) #self.db_table_layout_start_charges())

        # Create ListStore content for dropdown-Combobox
        if self.liststore_charge_templates == None:
            self.liststore_charge_templates = gtk.ListStore(int, str)
        self.update_comboboxes_in_treeview_charges()

       # Create 4 columns with the previous gtk.ListStore
        cell_renderer_combo_list = []
        for column_number in range(0, 4):
            cell_renderer_combo_list.append(gtk.CellRendererCombo())
            cell_renderer_combo_list[column_number].connect('edited', self.on_combocell_edited, self.liststore_charge_templates, column_number)
            cell_renderer_combo_list[column_number].set_property('editable', True)
            cell_renderer_combo_list[column_number].set_property('model', self.liststore_charge_templates)
            cell_renderer_combo_list[column_number].set_property('text-column', 1)


        treeview_column_list = []
        treeview_column_list.append(gtk.TreeViewColumn("fk_flight_type", gtk.CellRendererText(), text=0))
        treeview_column_list[0].set_visible(0)
        treeview_column_list.append(gtk.TreeViewColumn(unicode("Kürzel", "latin-1"), gtk.CellRendererText(), text=1))
        treeview_column_list.append(gtk.TreeViewColumn(unicode("Bemerkung", "latin-1"), gtk.CellRendererText(), text=2))
        treeview_column_list.append(gtk.TreeViewColumn(unicode("generelle Gebühr", "latin-1"), cell_renderer_combo_list[0], text=3))
        treeview_column_list.append(gtk.TreeViewColumn(unicode("bei Eigenstart", "latin-1"), cell_renderer_combo_list[1], text=4))
        treeview_column_list.append(gtk.TreeViewColumn(unicode("bei Windenstart", "latin-1"), cell_renderer_combo_list[2], text=5))
        treeview_column_list.append(gtk.TreeViewColumn(unicode("bei Schleppstart", "latin-1"), cell_renderer_combo_list[3], text=6))

        for treeview_column_number in xrange(len(treeview_column_list)):
            treeview_charges.append_column(treeview_column_list[treeview_column_number])

        liststore_charges = gtk.ListStore(int, str, str, str, str, str, str)

        # Connect all ListStoreColumns to the edited-event to catch the input
        for column_number in xrange(len(cell_renderer_combo_list)):
            cell_renderer_combo_list[column_number].connect('edited', self.on_treeview_charges_edited, liststore_charges, 3 + column_number)

        fk_flight_types_list = self.db_table_flight_types.get_column("pk_key_number")
        for fk_flight_type in fk_flight_types_list:
            flight_type_abbrevation = unicode(self.db_table_flight_types.search_column("pk_key_number", fk_flight_type, "abbrevation")[0], "latin-1")
            flight_type_note = unicode(self.db_table_flight_types.search_column("pk_key_number", fk_flight_type, "note")[0], "latin-1")

            liststore_charges.append([fk_flight_type, flight_type_abbrevation, flight_type_note, "-", "-", "-", "-"])
        liststore_charges.append([0, "-", "alle Flugarten", "-", "-", "-", "-"])
        treeview_charges.set_model(liststore_charges)
        return treeview_charges, liststore_charges

    def update_comboboxes_in_treeview_charges(self):
        charge_template_keys_list = self.db_table_charge_templates.get_column("pk_key_number")

        self.liststore_charge_templates.clear()
        self.liststore_charge_templates.append([0, "-"])
        if charge_template_keys_list <> None:
            for charge_template_key in charge_template_keys_list:
                charge_template_name = self.db_table_charge_templates.search_column('pk_key_number', charge_template_key, 'charge_template_name')[0]
                self.liststore_charge_templates.append([charge_template_key, unicode(charge_template_name, "latin-1")])

    def populate_treeview_start_charges(self, db_table_layout_list_parent):
        self.populate_treeview_charges(db_table_layout_list_parent, self.db_table_start_charges, self.treeview_start_charges)
        #self.db_portlet_table_start_charges_layout_list = db_portlet_table_layout_list

    def populate_treeview_landing_charges(self, db_table_layout_list_parent):
        self.populate_treeview_charges(db_table_layout_list_parent, self.db_table_landing_charges, self.treeview_landing_charges)
        #self.db_portlet_table_landing_charges_layout_list = db_portlet_table_layout_list

    def populate_treeview_charges(self, db_table_layout_list_parent, db_table, treeview):
        entry_key_number = get_widget_from_db_table_layout(db_table_layout_list_parent, "entry_key_number")
        self.pk_charges = entry_key_number.get_text()

        liststore_charges = treeview.get_model()

        for row_number in xrange(len(liststore_charges)):
            fk_flight_type_abbrevation = liststore_charges[row_number][0]
            table_dict = db_table.filter("fk_charge_name = " + self.pk_charges + " AND fk_flight_type_abbrevation = " + str(fk_flight_type_abbrevation))

            if len(table_dict) > 0:
                fk_general_charge = table_dict[0]['fk_general_charge']
                general_charge_dict = self.db_table_charge_templates.filter("pk_key_number = " + str(fk_general_charge))

                fk_self_start_charge = table_dict[0]['fk_self_start_charge']
                self_start_charge_dict = self.db_table_charge_templates.filter("pk_key_number = " + str(fk_self_start_charge))

                fk_winch_start_charge = table_dict[0]['fk_winch_start_charge']
                winch_start_charge_dict = self.db_table_charge_templates.filter("pk_key_number = " + str(fk_winch_start_charge))

                fk_tow_start_charge = table_dict[0]['fk_tow_start_charge']
                tow_start_charge_dict = self.db_table_charge_templates.filter("pk_key_number = " + str(fk_tow_start_charge))

                if len(general_charge_dict) > 0:
                    liststore_charges[row_number][3] = unicode(general_charge_dict[0]['charge_template_name'], 'latin-1')
                if len(self_start_charge_dict) > 0:
                    liststore_charges[row_number][4] = unicode(self_start_charge_dict[0]['charge_template_name'], 'latin-1')
                if len(winch_start_charge_dict) > 0:
                    liststore_charges[row_number][5] = unicode(winch_start_charge_dict[0]['charge_template_name'], 'latin-1')
                if len(tow_start_charge_dict) > 0:
                    liststore_charges[row_number][6] = unicode(tow_start_charge_dict[0]['charge_template_name'], 'latin-1')

    def populate_charge_simulator(self, db_table_layout_list_parent):
        # Let all the parts of the simulator be local objects!
        self.window_charges = self.form_window.get_widget("window_charges")
        self.class_charge.set_parent_window(self.window_charges)

        self.comboboxentry_booking_modality = self.form_window.get_widget("comboboxentry_booking_modality")
        self.comboboxentry_booking_modality.connect("changed", self.on_comboboxentry_simulator_changed)
        self.comboboxentry_flight_type = self.form_window.get_widget("comboboxentry_flight_type")
        self.comboboxentry_flight_type.connect("changed", self.on_comboboxentry_simulator_changed)

        self.comboboxentry_charge_template = self.form_window.get_widget("comboboxentry_charge_template")
        self.entry_flight_time = self.form_window.get_widget("entry_flight_time")
        self.entry_motor_runtime = self.form_window.get_widget("entry_motor_runtime")
        self.comboboxentry_tow_altitude = self.form_window.get_widget("comboboxentry_tow_altitude")
        self.entry_charge = self.form_window.get_widget("entry_charge")

        self.radiobutton_start_booking = self.form_window.get_widget("radiobutton_start_booking")
        self.radiobutton_start_booking.connect("toggled", self.on_comboboxentry_simulator_changed)
        self.radiobutton_landing_booking = self.form_window.get_widget("radiobutton_landing_booking")
        self.radiobutton_landing_booking.set_group(self.radiobutton_start_booking)
        self.radiobutton_landing_booking.connect("toggled", self.on_comboboxentry_simulator_changed)
        self.button_refresh = self.form_window.get_widget("button_refresh")
        self.button_refresh.connect("clicked", self.on_simulator_button_refresh_clicked)

        # Now, populate the comboboxentrys.
        booking_modality_list = []
        booking_modality_list.append([0, "generelle Gebühr"])
        booking_modality_list.append([1, "bei Eigenstart"])
        booking_modality_list.append([2, "bei Windenstart"])
        booking_modality_list.append([3, "bei Schleppstart"])
        populate_comboboxentry_from_list(self.comboboxentry_booking_modality, booking_modality_list, key_column=True)

        self.flight_type_abbrevation_list = self.db_table_flight_types.get_column_with_pk("abbrevation")
        populate_comboboxentry_from_list(self.comboboxentry_flight_type, self.flight_type_abbrevation_list, key_column=True)

        self.charge_template_list = self.db_table_charge_templates.get_column_with_pk("charge_template_name")
        populate_comboboxentry_from_list(self.comboboxentry_charge_template, self.charge_template_list, key_column=True)

    def save_treeview_start_charges(self):
        self.save_treeview_charges(self.db_table_start_charges, self.treeview_start_charges)

    def save_treeview_landing_charges(self):
        self.save_treeview_charges(self.db_table_landing_charges, self.treeview_landing_charges)

    def save_treeview_charges(self, db_table, treeview):
        liststore_charges = treeview.get_model()

        for treeview_column in liststore_charges:
            charge_content_dict = {}

            charge_content_dict["fk_charge_name"] = self.pk_charges
            charge_content_dict["fk_flight_type_abbrevation"] = treeview_column[0]
            charge_content_dict["fk_general_charge"] = self.get_liststore_key(treeview_column[3])
            charge_content_dict["fk_self_start_charge"] = self.get_liststore_key(treeview_column[4])
            charge_content_dict["fk_winch_start_charge"] = self.get_liststore_key(treeview_column[5])
            charge_content_dict["fk_tow_start_charge"] = self.get_liststore_key(treeview_column[6])
            db_table.delete_data(where="fk_charge_name = " + self.pk_charges + " AND " + \
                                       "fk_flight_type_abbrevation = " + str(treeview_column[0]))
            db_table.insert_data(content_dict = charge_content_dict)

    def get_liststore_key(self, cell_entry):
        for row_content in self.liststore_charge_templates:
            if cell_entry == row_content[1]:
                return row_content[0]

    # Dictionary database declaration -----------------------------------------
    def db_table_layout(self):
        db_table_layout_list = []

        db_table_layout_list.append({'db_field_name': 'pk_key_number', 'db_field_type': 'bigint'     , 'gtk_widget_name': 'entry_key_number' , 'gtk_treeview_column': 0, 'print_table_column': 0, 'db_primary_key': True, 'gtk_column_hide': True})
        db_table_layout_list.append({'db_field_name': 'charge_name'  , 'db_field_type': 'varchar(40)', 'gtk_widget_name': 'entry_charge_name', 'gtk_treeview_column': 1, 'print_table_column': 1, 'column_title': 'Gebührenbezeichnung'})

        db_table_layout_list.append({'db_field_name': 'deactivated'       , 'db_field_type': 'bool'        , 'gtk_widget_name': 'checkbutton_deactivated'      , 'gtk_treeview_column': 2, 'print_table_column': 2, 'gtk_column_hide': True})
        db_table_layout_list.append({'db_field_name': 'last_change_date'  , 'db_field_type': 'date'        , 'gtk_widget_name': None                           , 'gtk_treeview_column': 3, 'print_table_column': 3, 'gtk_column_hide': True})
        return db_table_layout_list

    def db_table_layout_start_charges(self):
        db_table_layout_list = []

        db_table_layout_list.append({'db_field_name': 'fk_charge_name'            , 'db_foreign_table': 'charges'         , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_name'            , 'gtk_treeview_column': 0, 'column_title': 'Gebührenbezeichnung'})
        db_table_layout_list.append({'db_field_name': 'fk_flight_type_abbrevation', 'db_foreign_table': 'flight_types'    , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'flight_type_abbrevation', 'gtk_treeview_column': 1, 'column_title': 'Flugart'})
        # ---------------------------------------------------------------------
        db_table_layout_list.append({'db_field_name': 'fk_general_charge'         , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 2, 'column_title': 'generell'})
        db_table_layout_list.append({'db_field_name': 'fk_self_start_charge'      , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 3, 'column_title': 'Eigenstart'})
        db_table_layout_list.append({'db_field_name': 'fk_winch_start_charge'     , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 4, 'column_title': 'Windenstart'})
        db_table_layout_list.append({'db_field_name': 'fk_tow_start_charge'       , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 5, 'column_title': 'Schleppstart'})
        return db_table_layout_list

    def db_table_layout_landing_charges(self):
        db_table_layout_list = []

        db_table_layout_list.append({'db_field_name': 'fk_charge_name'            , 'db_foreign_table': 'charges'         , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_name'            , 'gtk_treeview_column': 0, 'column_title': 'Gebührenbezeichnung'})
        db_table_layout_list.append({'db_field_name': 'fk_flight_type_abbrevation', 'db_foreign_table': 'flight_types'    , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'flight_type_abbrevation', 'gtk_treeview_column': 1, 'column_title': 'Flugart'})
        # ---------------------------------------------------------------------
        db_table_layout_list.append({'db_field_name': 'fk_general_charge'         , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 2, 'column_title': 'generell'})
        db_table_layout_list.append({'db_field_name': 'fk_self_start_charge'      , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 3, 'column_title': 'Eigenstart'})
        db_table_layout_list.append({'db_field_name': 'fk_winch_start_charge'     , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 4, 'column_title': 'Windenstart'})
        db_table_layout_list.append({'db_field_name': 'fk_tow_start_charge'       , 'db_foreign_table': 'charge_templates', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'charge_template_name'   , 'gtk_treeview_column': 5, 'column_title': 'Schleppstart'})
        return db_table_layout_list

    def db_layout_dictlist_charge_templates(self):
        db_table_layout_list = []

        db_table_layout_list.append({'db_field_name': 'pk_key_number'       , 'db_field_type': 'bigint'        , 'gtk_widget_name': 'entry_key_number'             , 'gtk_treeview_column': 0, 'print_table_column': 0, 'db_primary_key': True, 'gtk_column_hide': True})
        db_table_layout_list.append({'db_field_name': 'charge_template_name', 'db_field_type': 'varchar(60)'   , 'gtk_widget_name': 'entry_charge_template_name'   , 'gtk_treeview_column': 1, 'print_table_column': 1, 'column_title': 'Name Gebührenvorlage'})
        db_table_layout_list.append({'db_field_name': 'charge_template_code', 'db_field_type': 'varchar(65536)', 'gtk_widget_name': 'textview_charge_template_code', 'gtk_treeview_column': 2, 'print_table_column': 2, 'column_title': 'Quellcode Vorlage'})

        db_table_layout_list.append({'db_field_name': 'deactivated'       , 'db_field_type': 'bool'        , 'gtk_widget_name': 'checkbutton_deactivated'      , 'gtk_treeview_column': 3, 'print_table_column': 3, 'gtk_column_hide': True})
        db_table_layout_list.append({'db_field_name': 'last_change_date'  , 'db_field_type': 'date'        , 'gtk_widget_name': None                           , 'gtk_treeview_column': 4, 'print_table_column': 4, 'gtk_column_hide': True})
        return db_table_layout_list


class charge:
    def __init__(self, DBcnx):
        self.db_table_charges = db_table(DBcnx, "charges")
        self.db_table_flight_types = db_table(DBcnx, "flight_types")
        self.db_table_start_charges = db_table(DBcnx, "start_charges")
        self.db_table_landing_charges = db_table(DBcnx, "landing_charges")
        self.db_table_charge_templates = db_table(DBcnx, "charge_templates")
        self.parent_window = None

    def set_parent_window(self, parent_window):
        self.parent_window = parent_window

    def get_charge_template(self, pk_charge, booking_modality, pk_flight_type, start=False, landing=False):
        if start == True:
            db_table = self.db_table_start_charges
        if landing == True:
            db_table = self.db_table_landing_charges

        if booking_modality == 0: booking_modality = "fk_general_charge"
        if booking_modality == 1: booking_modality = "fk_self_start_charge"
        if booking_modality == 2: booking_modality = "fk_winch_start_charge"
        if booking_modality == 3: booking_modality = "fk_tow_start_charge"
        #print "booking_modality:", booking_modality

        if booking_modality <> ():
            charge_template_result = db_table.filter("fk_charge_name = " + str(pk_charge) + " AND " + booking_modality + " = " + str(pk_flight_type))
            #print "charge_template_result", charge_template_result
        else:
            return

        if len(charge_template_result) > 0:
            pk_charge_template = charge_template_result[0][booking_modality]
            #print "pk_charge_template", pk_charge_template
            return pk_charge_template
        return

    def calculate_from_template(self, pk_charge_template, flight_time=0, motor_runtime=0, tow_altitude=0):
        charge_template_code = self.db_table_charge_templates.search_column("pk_key_number", pk_charge_template, "charge_template_code")[0]
        #print "charge_template_code...", charge_template_code
        try:
            if charge_template_code <> ():
                exec(charge_template_code)
                return charge
            else:
                return 0
        except Exception, inst:
            dialog(parent=self.parent_window, label_text=str(inst))
        return

