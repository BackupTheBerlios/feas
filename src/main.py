# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS main program V0.8 alpha
# (c) by Mark Muzenhardt
#===============================================================================

import time, datetime
import gtk.glade, gobject

import flight_calculator

# Import all the modern magic FEAS got...
import options
import person
import calendar
import aircraft
import user_group
import charge

# ... and the older magic FEAS has to overcome!
import flight_recording
import flight_permissions
import flight_control
import user_group
import licenses
import flight_types
import time_setting
import flight_sectors
# import starting_types

# Code cleaning with the new generation modules! ------------------------------
from BaseUI.DB import SQLdb
from BaseUI.GTK import Widgets, Glade, Dialogs, DataViews
from BaseUI.Commons import Sun, DateTime, FileSystem, HelpFile
from BaseUI import Portlets
from config import *


class application:
    def __init__(self):
        self.window_start = window_start()
        
        
        
class window_start:
    def __init__(self):
        # New login dialog...
        self.wTree = Glade.import_tree(self, RESOURCE_DIR + 'main.glade', 'window_start')
        self.window_start = self.wTree.get_widget('window_start')
        self.DialogBox = Dialogs.Simple(parent=self.window_start)
        self.notebook_start = self.wTree.get_widget("notebook_start")
        
        self.togglebutton_preferences_new = self.wTree.get_widget('togglebutton_preferences_new')
        self.button_forward = self.wTree.get_widget('button_forward')
        self.button_backward = self.wTree.get_widget('button_backward')
        
        self.table_user = self.wTree.get_widget('table_user')
        self.table_flight_permissions = self.wTree.get_widget('table_flight_permissions')
        self.table_flight_control = self.wTree.get_widget('table_flight_control')
        
        # Offsets to set the correct widgets sensitive or not.
        self.quit_offset = False
        self.login_offset = True
        self.dfs_offset = True
        self.flight_control_offset = True

        self.initialize_login()
        self.initialize_flight_permissions()
        self.initialize_flight_control()
        self.window_start.show_all()
        
        # Connects the database.
        self.database_dialog = Portlets.DatabaseLogin(ini_filename=USER_DIR + "settings.ini", parent=self.window_start)
        self.database_portlet = self.database_dialog.portlet
        self.database_dialog.set_connect_function(self.on_connect)
        self.database_dialog.set_disconnect_function(self.on_disconnect)
        self.database = self.database_dialog.database
        self.database_dialog.connect()
        
        
    # Callbacks ----------------------------------------------------------------
    def on_togglebutton_preferences_new_toggled(self, widget=None, data=None):
        if widget.get_active():
            self.vbox_user.remove(self.image)
            self.vbox_user.pack_start(self.database_portlet)
            self.window_start.show_all()
        else:
            self.vbox_user.remove(self.database_portlet)
            self.vbox_user.pack_start(self.image)
            
            
    def on_notebook_start_switch_page(self, widget=None, pointer=None, page=None):
        self.set_buttons(page)
        
        
    def on_button_forward_clicked(self, widget=None, data=None):
        if widget.get_label() == gtk.STOCK_OK:
            self.on_ok()
            return
        
        if self.current_page == 0:
            if self.validate_login() <> True:
                return
                
        self.notebook_start.next_page()
        self.set_buttons()
        
        
    def on_button_backward_clicked(self, widget=None, data=None):
        if widget.get_label() == gtk.STOCK_CANCEL:
            self.on_cancel()

        self.notebook_start.prev_page()
        self.set_buttons()
        
        
    def on_button_cancel_clicked(self, widget=None, data=None):
        self.window_start.destroy()
        
        
    def on_window_start_destroy(self, widget=None, data=None):
        if self.quit_offset == False: 
            self.quit()
            
            
    # Actions -----------------------------------------------------------------
    def on_ok(self):
        self.database_dialog.save_settings_to_ini()
        self.quit_offset = True
        self.window_start.destroy()
        self.quit_offset = False
        
        try:
            self.window_main = window_main(self.database, self.user_selection)
        except Exception, inst:
            raise
            #self.DialogBox.show(dialog_type='error', title="Fehler", inst=inst)
            self.quit()
            
            
    def on_cancel(self):
        self.window_start.destroy()
        
        
    def on_connect(self):
        self.button_forward.set_sensitive(1)
        self.database = self.database_dialog.database
        self.populate_login()
        self.populate_flight_permissions()
        self.populate_flight_control()
        
        
    def on_disconnect(self):
        self.button_forward.set_sensitive(0)
        self.togglebutton_preferences_new.set_active(1)
        self.database = self.database_dialog.database
        
        
    def set_buttons(self, current_page=None):
        self.current_page = current_page
        pages = self.notebook_start.get_n_pages()
        label_button_backward = self.button_backward.get_label()
        label_button_forward = self.button_forward.get_label()
        
        if self.current_page == None:
            self.current_page = self.notebook_start.get_current_page()
        if self.current_page == 0:
            self.button_backward.set_label(gtk.STOCK_CANCEL)
            self.togglebutton_preferences_new.set_sensitive(True)
        else:
            self.button_backward.set_label(gtk.STOCK_GO_BACK)
            self.togglebutton_preferences_new.set_sensitive(False)
        if self.current_page == (pages-1):
            self.button_forward.set_label(gtk.STOCK_OK)
        else:
            self.button_forward.set_label(gtk.STOCK_GO_FORWARD)
        if self.current_page == 1:
            self.table_flight_permissions.set_sensitive(1)
        if self.current_page == 2:
            self.table_flight_control.set_sensitive(1)
            
            
    def validate_login(self):
        self.user_selection = self.login_dialog.comboboxentry_user.get_selection()
        password = self.login_dialog.entry_password.get_text()
        
        if self.user_selection == None:
            self.DialogBox.show(dialog_type='warning', text='Kein Benutzer ausgewählt!')
            return False
        else:
            if self.user_selection['password'] <> None and \
                self.user_selection['password'] <> password:
                self.DialogBox.show(dialog_type='warning', text='Passwort ist nicht korrekt!')
                return False
        return True
    
            
    # Login portlet ------------------------------------------------------------
    def initialize_login(self):
        self.vbox_user = self.wTree.get_widget('vbox_user')

        self.image = gtk.Image()
        self.image.set_from_file(RESOURCE_DIR + 'about.svg')
        self.vbox_user.add(self.image)

        # This makes the user login
        self.login_dialog = Portlets.UserLogin(parent=self.window_start)
        self.login_portlet = self.login_dialog.portlet
        self.vbox_user.pack_end(self.login_portlet, expand=False, fill=True)
        
        
    def populate_login(self):
        # Populates the Login-Widgets
        self.db_table_person = person.db_table_person(self.database)
        user_lod = self.db_table_person.select(column_list=['id', 'firstname', 'lastname', 'password'])
        
        if user_lod == []:
            user_lod = [{'id': None, 'firstname': 'admin', 'lastname': '', 'password': None}]
        self.login_dialog.populate(content_lod=user_lod, merge_field_list=['lastname', 'firstname'])
        self.set_buttons()
        
    
    # DFS portlet --------------------------------------------------------------
    def initialize_flight_permissions(self):
        self.alignment_flight_permissions = self.wTree.get_widget('alignment_flight_permissions')
        
        self.flight_permissions_main = flight_permissions.main()
        self.flight_permissions_portlet = self.flight_permissions_main.portlet
        self.alignment_flight_permissions.add(self.flight_permissions_portlet)
        
        
    def populate_flight_permissions(self):
        pass

    
    # Flight control portlet ---------------------------------------------------
    def initialize_flight_control(self):
        self.alignment_flight_control = self.wTree.get_widget('alignment_flight_control')
        
        self.flight_control_main = flight_control.main()
        self.flight_control_portlet = self.flight_control_main.portlet
        self.alignment_flight_control.add(self.flight_control_portlet)
        
    
    def populate_flight_control(self):
        pass

    
    def quit(self):
        if self.database.connection <> None:
            self.database.close()
        gtk.main_quit()



# Main application window class ------------------------------------------------
class window_main:
    def __init__(self, database, user_dic=None):
        if user_dic == None:
            raise Exception('Kein Benutzer ausgewählt!')
        
        self.database = database
        self.user_dic = user_dic

        self.wTree = Glade.import_tree(self, RESOURCE_DIR + "main.glade", "window_main")
        self.window_main = self.wTree.get_widget("window_main")
        self.window_main.set_gravity(gtk.gdk.GRAVITY_CENTER)
        self.window_main.resize(800, 600)
        self.window_main.set_title(APP_NAME)

        self.toolbar_main = self.wTree.get_widget("toolbar_main")
        self.main_toolbar = self.toolbar_main
        self.hbox_main = self.wTree.get_widget("hbox_main")
        self.vbox_main = self.wTree.get_widget("vbox_main")
        self.button_change_user = self.wTree.get_widget("button_change_user")

        self.sun = Sun.Sun()
        self.DialogBox = Dialogs.Simple(parent=self.window_main)
        self.HTMLhelp = HelpFile.HTML()

        # Portlets -------------------------------------------------------------
        #self.portlet_flight_control = flight_control.portlet_flight_controler(self.database)
        #self.db_table_flight_controler_log = db_table(self.DBcnx, "flight_controler_log")
        #self.db_table_layout_flight_controler_log = self.portlet_flight_controler.db_table_layout
        self.get_portlets()

        self.portlet_upper_tooltable = self.wTree.get_widget("scrolledwindow_upper_tooltable")
        self.portlet_lower_tooltable = self.wTree.get_widget("scrolledwindow_lower_tooltable")

        # Makes the upper tooltable portlet white for better looking.
        self.layout_upper_tooltable = self.wTree.get_widget('layout_upper_tooltable')
        self.layout_upper_tooltable.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65535, 65535, 65535))

        self.entry_time = self.wTree.get_widget('entry_time')
        self.entry_date = self.wTree.get_widget('entry_date')
        self.entry_flight_traffic_leader = self.wTree.get_widget('entry_flight_traffic_leader')
        self.entry_sunrise = self.wTree.get_widget('entry_sunrise')
        self.entry_sunset = self.wTree.get_widget('entry_sunset')
        self.setup_upper_left_portlet()

        # TODO: Make the lower tooltable portlet an autonome module.
        self.treeview_lower_tooltable = self.wTree.get_widget("treeview_lower_tooltable")
        self.treeview_lower_tooltable.set_enable_tree_lines(True)
        #self.treeview_lower_tooltable.set_level_indentation(16)

        self.hseparator = self.wTree.get_widget("hseparator")
        self.vseparator = self.wTree.get_widget("vseparator")

        self.window_main.show()
        self.message_id = None
        self.setup_lower_left_portlet()

        # Setup preferences and the like ---------------------------------------
        self.window_options = options.main(self.database)
        self.window_flight_calulator = flight_calculator.main()


    # Menubar ------------------------------------------------------------------
    #TODO: There are several menu items, that have to be added
    def on_menuitem_preferences_activate(self, widget=None, data=None):
        self.window_options.initGUI()


    def on_menuitem_calculator_activate(self, widget=None, data=None):
        self.window_flight_calulator.initGUIwindow()


    def on_menuitem_quit_activate(self, widget=None, data=None):
        self.window_main.destroy()


    # --------------------------------------------------------------------------
    def on_menuitem_about_activate(self, widget=None, data=None):
        self.show_about_dialog()


    def on_menuitem_help_activate(self, widget=None, data=None):
        self.show_help()


    # Toolbar ------------------------------------------------------------------
    def on_button_about_clicked(self, widget=None, data=None):
        self.show_about_dialog()


    def on_window_main_destroy(self, widget=None, data=None):
        self.quit()


    def on_window_main_delete_event(self, widget, data=None):
        login_dict = {}
        #login_dict['logout_date'] = get_usdate_str()
        #login_dict['logout_time'] = get_gmtime_str()
        #self.db_table_flight_controler_log.update_data(self.login_pk, self.db_table_layout_flight_controler_log(), login_dict)
        return False # True, if window should not be deleted with close button!


    def on_button_print_preview_clicked(self, widget=None):
        #filename = None

        #if self.selected_item == "Mitglieder":
        #    filename = self.table_portlet_members.build_report()

        #if filename <> None:
        #    startbrowser(filename)

        if DEBUG: print "print preview", self.selected_item, "clicked"


    def on_button_change_user_clicked(self, widget=None, data=None):
        print "user change"


    # Help dialog -------------------------------------------------------------
    def show_about_dialog(self):
         text = """\
<u><b>FEAS 2008</b></u>

Programmiert von: <b>Mark Muzenhardt</b>
für den <b>Aeroclub Fürth e.V.</b>

Dieses Programm steht unter der freien <b>BSD-Lizenz</b>.
Somit darf es frei von Lizenzgebühren weitergegeben und
verändert werden."""

         self.DialogBox.show(dialog_type='info', title="Über...", text=text)


    def show_help(self):
        self.HTMLhelp.show('user/first_steps.html')


    # -------------------------------------------------------------------------
    def on_treeview_lower_tooltable_cursor_changed(self, widget=None, data=None):
        row_dic = self.TableLeft.get_selected_row_content()
        self.selected_item = row_dic['name']
        
        # TODO: This lines could be handled by a config-module
        if self.selected_item == u"Erfassung":
            self.open_main_portlet(self.flight_recording_main)
        elif self.selected_item == u"Flugzeuge":
            self.open_main_portlet(self.aircraft_main)
        elif self.selected_item == u"Gebühren":
            self.open_main_portlet(self.charge_main)
        elif self.selected_item == u"Personen":
            self.open_main_portlet(self.person_main)
        elif self.selected_item == u"Kalender":
            self.open_main_portlet(self.calendar_main)
        else:
            self.open_main_portlet(None)


    def open_main_portlet(self, main_object=None):
        if self.portlet_main <> None:
            self.hbox_main.remove(self.portlet_main)
            self.portlet_main = None

        if self.main_toolbar <> None:
            self.vbox_main.remove(self.main_toolbar)
            self.main_toolbar = None

        if main_object <> None:
            self.portlet_main = main_object.portlet
            self.hbox_main.pack_start(self.portlet_main)
            main_object.update()
            if main_object.toolbar <> None:
                self.main_toolbar = main_object.toolbar
        else:
            self.main_toolbar = self.toolbar_main

        self.vbox_main.pack_start(self.main_toolbar, expand=False)
        self.vbox_main.reorder_child(self.main_toolbar, 1)
        self.window_main.show_all()


    def set_time_entry(self):
        gmtime = time.strftime('%H:%M:%S', time.gmtime())
        gmdate = time.strftime('%d.%m.%Y', time.gmtime())

        self.entry_time.set_text(gmtime)
        self.entry_date.set_text(gmdate)

        utc_now = datetime.datetime.utcnow()

        year = utc_now.year
        month = utc_now.month
        day = utc_now.day

        lat = 49.00
        lon = 11.00
        sunrise, sunset = self.sun.sunRiseSet(year, month, day, lon, lat)

        h, m, s = self.sun.decimal_to_hms(sunrise)
        sunrise_timestr = "%02i:%02i:%02i" % (h, m, s)
        self.entry_sunrise.set_text(sunrise_timestr)

        h, m, s = self.sun.decimal_to_hms(sunset)
        sunset_timestr = "%02i:%02i:%02i" % (h, m, s)
        self.entry_sunset.set_text(sunset_timestr)
        return True


    def setup_upper_left_portlet(self):
        #print self.user_dic
        self.entry_flight_traffic_leader.set_text(self.user_dic['#merged_fields'])
        gobject.timeout_add(1000, self.set_time_entry)


    def setup_lower_left_portlet(self):
        definition_lod = \
        [
            {'column_name': 'picture',
             'data_type': '#image',
             'column_label': 'Bild',
             'column_number': 0,
             'visible': True,
             'editable': False,
             'expand': False,
             'sortable': False,
             'resizeable': False},
            {'column_name': 'name',
             'data_type': 'varchar',
             'column_label': 'Name',
             'column_number': 1,
             'visible': True,
             'editable': False,
             'sortable': False,
             'resizeable': True,
             'reorderable': True,
             'expand': False}
        ]

        content_lod = \
        [
            {'name': 'Erfassung',   'picture': RESOURCE_DIR + "report_32.png"},
            {'name': 'Flugleitung', 'picture': RESOURCE_DIR + "tower_32.png"},
            {'name': 'Stammdaten',  'picture': RESOURCE_DIR + "folder_32.png", '#child':
            [
                {'name': 'Personen',  'picture': RESOURCE_DIR + "person_32.png"},
                {'name': 'Flugzeuge', 'picture': RESOURCE_DIR + "aircraft_32.png"},
                {'name': u'Gebühren', 'picture': RESOURCE_DIR + "euro_32.png"}
            ]}
        ]

        try:
            self.TableLeft = DataViews.Tree(self.treeview_lower_tooltable)
            self.TableLeft.initialize(definition_lod)
            self.TableLeft.populate(content_lod)
            self.treeview_lower_tooltable.set_cursor(0)
        except Exception, inst:
            self.DialogBox.show(dialog_type="error", title="Fehler", text=str(inst))


    # --------------------------------------------------------------------------
    def get_portlets(self):
        self.person_main = person.main(self.database)
        self.calendar_main = calendar.main(self.database)
        self.flight_recording_main = flight_recording.main(self.database)
        self.aircraft_main = aircraft.main(self.database)
        self.user_group_main = user_group.main(self.database)
        self.charge_main = charge.main(self.database)
        
        self.portlet_main = None


    def quit(self):
        self.database.close()
        #close_db(self.DBcnx)
        gtk.main_quit()




