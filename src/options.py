# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS options module. Introduced in v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import flight_types
import flight_directives

from BaseUI import Portlets
from BaseUI.DB import SQLdb
from BaseUI.GTK import Glade, Dialogs
from config import *


class main:
    def __init__(self, db_object=None):
        self.DialogBox = Dialogs.Simple()
        
        self.db_object = db_object
        self.db_table = db_table(self.db_object)
        
        self.db_table_runways = db_table_runways(self.db_object)
        self.form_runways = form_runways(self.db_object)
        self.table_runways = table_runways(self.db_object, self.form_runways)
        self.portlet_runways = self.table_runways.portlet
        
        self.db_table_clubs = db_table_clubs(self.db_object)
        self.form_clubs = form_clubs(self.db_object)
        self.table_clubs = table_clubs(self.db_object, self.form_clubs)
        self.portlet_clubs = self.table_clubs.portlet
        
        self.db_table_user_groups = db_table_user_groups(self.db_object)
        self.form_user_groups = form_user_groups(self.db_object)
        self.table_user_groups = table_user_groups(self.db_object, self.form_user_groups)
        self.portlet_user_groups = self.table_user_groups.portlet
        
        self.flight_types_main = flight_types.main(self.db_object)
        self.portlet_flight_types = self.flight_types_main.portlet
        
        self.flight_directives_main = flight_directives.main(self.db_object)
        self.portlet_flight_directives = self.flight_directives_main.portlet
                
        
    def initGUI(self):
        self.wTree = Glade.import_tree(self, RESOURCE_DIR + "main.glade", "window_options")
        self.window_options = self.wTree.get_widget("window_options")
        self.DialogBox.set_parent(self.window_options)
        
        self.alignment_runways = self.wTree.get_widget('alignment_runways')
        self.alignment_runways.add(self.portlet_runways)
        
        self.alignment_clubs = self.wTree.get_widget('alignment_clubs')
        self.alignment_clubs.add(self.portlet_clubs)
        
        self.alignment_user_groups = self.wTree.get_widget('alignment_user_groups')
        self.alignment_user_groups.add(self.portlet_user_groups)
        
        self.alignment_flight_types = self.wTree.get_widget('alignment_flight_types')
        self.alignment_flight_types.add(self.portlet_flight_types)
        
        self.alignment_flight_directives = self.wTree.get_widget('alignment_flight_directives')
        self.alignment_flight_directives.add(self.portlet_flight_directives)
        self.window_options.show_all()


    # Footbar button events ---------------------------------------------------
    def on_button_ok_clicked(self, widget=None, data=None):
        self.save_settings()
        self.window_options.destroy()


    def on_button_cancel_clicked(self, widget=None, data=None):
        self.window_options.destroy()
        
    
    def on_window_options_destroy(self, widget=None, data=None):
        self.alignment_runways.remove(self.portlet_runways)
        self.alignment_clubs.remove(self.portlet_clubs)
        self.alignment_flight_types.remove(self.portlet_flight_types)
        self.alignment_user_groups.remove(self.portlet_user_groups)
        
    
    def save_settings(self):
        print "save not yet implemented"
        


class db_table(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',        'data_type': 'bigint' , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'module',    'data_type': 'varchar', 'character_maximum_length': 40, 'column_number':    0, 'column_label': 'Modul'},
        {'column_name': 'attribute', 'data_type': 'varchar', 'character_maximum_length': 40, 'column_number':    1, 'column_label': 'Option'},
        {'column_name': 'value',     'data_type': 'varchar', 'character_maximum_length': 40, 'column_number':    2, 'column_label': 'Wert'},
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'options')
        differences_lod = self.check_attributes(self.attributes, add=True)



# Runways ----------------------------------------------------------------------
class db_table_runways(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',                'data_type': 'bigint' , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'description',       'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'runway_designator', 'data_type': 'varchar', 'character_maximum_length':  3},
        {'column_name': 'type',              'data_type': 'varchar', 'character_maximum_length': 40}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'runways')
        differences_lod = self.check_attributes(self.attributes, add=True)



class form_runways(Portlets.Form):
    definition = \
    [
        {'column_name': 'description',       'widget_name': 'entry_description'},
        {'column_name': 'runway_designator', 'widget_name': 'entry_runway_designator'},
        {'column_name': 'type',              'widget_name': 'entry_type'}
    ]

    def __init__(self, db_object):
        self.db_object = db_object
        self.db_table = db_table_runways(self.db_object)

        Portlets.Form.__init__(self, icon_file=RESOURCE_DIR + 'runway_22.png', title='Pisten', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_runway', help_file='user/options.html')
        self.attributes_lod = self.db_table.attributes
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod='')



class table_runways(Portlets.Table):
    definition = \
    [
        {'column_name': 'id',                'column_number':  0, 'visible': False},
        {'column_name': 'description',       'column_number':  2, 'column_label': 'Beschreibung'},
        {'column_name': 'runway_designator', 'column_number':  1, 'column_label': 'Pistenkennung'},
        {'column_name': 'type',              'column_number':  3, 'column_label': 'Typ'}
    ]

    def __init__(self, db_object, form_object):
        self.db_object = db_object
        self.db_table = db_table_runways(self.db_object)

        Portlets.Table.__init__(self, form_object, filter=False, help=False, separate_toolbar=False)
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition)

        self.Table.set_sort_column('runway_designator')
        
        
        
# Clubs on the airfield --------------------------------------------------------
class db_table_clubs(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',   'data_type': 'bigint' , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'name', 'data_type': 'varchar', 'character_maximum_length': 40}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'clubs')
        differences_lod = self.check_attributes(self.attributes, add=True)



class form_clubs(Portlets.Form):
    definition = \
    [
        {'column_name': 'name', 'widget_name': 'entry_name'}
    ]

    def __init__(self, db_object):
        self.db_object = db_object
        self.db_table = db_table_clubs(self.db_object)

        Portlets.Form.__init__(self, icon_file=RESOURCE_DIR + 'member_16.png', title='Vereine', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_club', help_file='user/options.html')
        self.attributes_lod = self.db_table.attributes
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod='')



class table_clubs(Portlets.Table):
    definition = \
    [
        {'column_name': 'id',   'column_number': 0, 'visible': False},
        {'column_name': 'name', 'column_number': 1, 'column_label': 'Name'}
    ]

    def __init__(self, db_object, form_object):
        self.db_object = db_object
        self.db_table = db_table_clubs(self.db_object)

        Portlets.Table.__init__(self, form_object, filter=False, help=False, separate_toolbar=False)
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition)

        self.Table.set_sort_column('name')



# User groups ------------------------------------------------------------------
class db_table_user_groups(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id',         'data_type': 'bigint' , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'user_group', 'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'password',   'data_type': 'varchar', 'character_maximum_length': 128}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'user_groups')
        differences_lod = self.check_attributes(self.attributes, add=True)



class form_user_groups(Portlets.Form):
    definition = \
    [
        {'column_name': 'user_group', 'widget_name': 'entry_user_group'},
        {'column_name': 'password',   'widget_name': 'entry_password'}
    ]

    def __init__(self, db_object):
        self.db_object = db_object
        self.db_table = db_table_user_groups(self.db_object)

        Portlets.Form.__init__(self, icon_file=RESOURCE_DIR + 'user_group_16.png', title='Benutzergruppen', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_user_group', help_file='user/options.html')
        self.attributes_lod = self.db_table.attributes
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod='')



class table_user_groups(Portlets.Table):
    definition = \
    [
        {'column_name': 'id',         'column_number': 0, 'visible': False},
        {'column_name': 'user_group', 'column_number': 1, 'column_label': 'Benutzergruppe'}
    ]

    def __init__(self, db_object, form_object):
        self.db_object = db_object
        self.db_table = db_table_user_groups(self.db_object)

        Portlets.Table.__init__(self, form_object, filter=False, help=False, separate_toolbar=False)
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition)

        self.Table.set_sort_column('user_group')



