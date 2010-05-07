# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS flight_recording module. Fully reviewed for v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

import gobject, gtk
import time

import aircraft
import person
import charge
import options

from BaseUI import Portlets
from BaseUI.DB import SQLdb
from BaseUI.GTK import Glade, Entrys
from config import *

DEBUG = False

if DEBUG:
    from pprint import pprint
    

class main:
    def __init__(self, db_object):
        self.db_object = db_object
        self.db_table = db_table(self.db_object)
        
        self.ui_form = ui_form(self.db_object)
        self.ui_table = ui_table(self.db_object, self.ui_form)

        self.wTree = Glade.import_tree(self, RESOURCE_DIR + 'portlets.glade', 'portlet_flight_recording')
        self.window = self.wTree.get_widget('portlet_flight_recording')
        self.alignment_flight_record = self.wTree.get_widget("alignment_flight_record")
        self.alignment_flight_record.add(self.ui_table.portlet)

        self.window_aircraft_selection = window_aircraft_selection(self.db_object, self.ui_table)

        # Cut portlet out of window
        self.portlet = self.window.get_child()
        self.window.remove(self.portlet)
        self.window.destroy()

        self.toolbar = self.ui_table.toolbar


    def on_button_start_clicked(self, widget=None):
        self.window_aircraft_selection.setup_start()


    def on_button_landing_clicked(self, widget=None):
        self.window_aircraft_selection.setup_landing()


    def on_button_edit_flight_record_clicked(self, widget=None):
        print 'edit'
        #key_number = self.table_portlet_flight_record.get_selected_item()
        #if key_number <> None:
        #    self.table_portlet_flight_record.edit_dataset(key_number)


    def update(self):
        self.ui_table.update()
    


class flight:
    def __init__(self, db_object):
        pass


    def start(self):
        pass


    def finish(self):
        pass



class window_aircraft_selection:
    def __init__(self, db_object=None, ui_table=None):
        self.db_object = db_object
        self.ui_table = ui_table
        
        self.action = None
        self.selection = None
        self.sailplane_1_dic = None
        self.sailplane_2_dic = None
        
        self.db_table_aircraft = aircraft.db_table_aircraft(self.db_object)
                

    def show(self):
        self.wTree = Glade.import_tree(self, RESOURCE_DIR + 'forms.glade', 'window_aircraft_selection')
        self.window = self.wTree.get_widget('window_aircraft_selection')
        self.window.set_keep_above(True)
        self.window.show()

        self.comboboxentry_aircraft_id = Entrys.Combobox(widget=self.wTree.get_widget('comboboxentry_aircraft_id'))
        self.comboboxentry_aircraft_id.connect('changed', self.on_comboboxentry_aircraft_changed)

        self.button_dict = {'button_1': self.wTree.get_widget('button_1'),
                            'button_2': self.wTree.get_widget('button_2'),
                            'button_3': self.wTree.get_widget('button_3'),
                            'button_4': self.wTree.get_widget('button_4')}

        self.button_dict['button_1'].set_label('_Fremd LFZ')
        self.button_dict['button_1'].show()
        self.button_dict['button_4'].set_label('_Abbruch')
        self.button_dict['button_4'].show()
        
        self.window_aircraft_selection = window_aircraft_selection(self.db_object, self.ui_table)
        self.window_start_record = window_start_record(self.db_object, self.ui_table)
        self.window_landing_record = window_landing_record(self.db_object, self.ui_table)
        

    # Widget signals ----------------------------------------------------------
    def on_comboboxentry_aircraft_changed(self, widget=None):
        self.selection = self.comboboxentry_aircraft_id.get_selection()
        if self.selection == None:
            return
        else:
            self.set_buttons()
            
         
    def on_button_clicked(self, widget=None):
        button_label = widget.get_label()
        button_name = widget.get_name()
        print button_label, button_name

        if button_label in ['_F-Schlepp', '_Windenstart', '_Eigenstart']:
            self.window.destroy()
                
        if self.action == "start":
            if button_label == '_F-Schlepp':
                self.window_aircraft_selection.show()
                self.window_aircraft_selection.setup_tow(self.selection)
            elif button_label == "_Windenstart":
                self.window_start_record.show()
                self.window_start_record.setup_winch_start(self.selection)
            elif button_label == "_Eigenstart":
                self.window_start_record.show()
                self.window_start_record.setup_self_start(self.selection)
            if button_label == "_Fremd LFZ":
                print "Not yet implemented!"
        
        if self.action == "tow":
            if button_label == "_F-Schlepp":
                self.window_start_record.show()
                self.window_start_record.setup_tow_start(self.selection, self.sailplane_1_dic)
        
        if self.action == "landing":
            if button_label == "_Landung":
                self.window.destroy()
                self.window_landing_record = window_landing_record(self.db_object, self.table_portlet)
                #self.window_landing_record.show()
                self.window_landing_record.setup_landing(self.selection)

        if button_label == "_Abbruch":
            self.window.destroy()


    # main functions ----------------------------------------------------------
    def set_buttons(self):
        self.button_dict['button_1'].hide()
        self.button_dict['button_2'].hide()
        self.button_dict['button_3'].hide()
        
        button_list = []
        if self.action == "start":    
            if self.selection.has_key('self_start'):
                if self.selection['self_start']:
                    button_list.append('_Eigenstart')
                if self.selection.has_key('bow_tow_clutch'):
                    if self.selection['bow_tow_clutch']:
                        button_list.append('_F-Schlepp')
                if self.selection.has_key('center_tow_clutch'):
                    if self.selection['center_tow_clutch']:
                        if '_F-Schlepp' not in button_list:
                            button_list.append('_F-Schlepp')
                        button_list.append('_Windenstart')               
            
        if self.action == "tow":
            button_list.append("_F-Schlepp")
            
        if self.action == "landing":
            button_list.append("_Landung")
            
        for button in enumerate(button_list):
            button_no = button[0] + 1 
            self.button_dict['button_%i' % button_no].set_label(button[1])
            self.button_dict['button_%i' % button_no].show()
        
        
    def setup_start(self):
        self.show()
        self.window.set_title("Bitte startendes Flugzeug eingeben...")
        
        aircraft_on_ground_lod = self.db_table_aircraft.get_aircraft_on_ground()
        self.comboboxentry_aircraft_id.initialize(definition_dic={'column_name': ['aircraft_id', 'aircraft_pattern'], 'mask': '%(aircraft_id)s - %(aircraft_pattern)s'},
                                                  attributes_lod=self.db_table_aircraft.attributes)
        self.comboboxentry_aircraft_id.populate(aircraft_on_ground_lod)
        self.action = "start"        


    def setup_tow(self, sailplane_1_dic):
        self.sailplane_1_dic = sailplane_1_dic
        
        self.window.set_title("Bitte Schlepp-Flugzeug eingeben...")
        
        aircraft_on_ground_lod = self.db_table_aircraft.get_aircraft_on_ground()
        self.comboboxentry_aircraft_id.initialize(definition_dic={'column_name': ['aircraft_id', 'aircraft_pattern'], 'mask': '%(aircraft_id)s - %(aircraft_pattern)s'},
                                                  attributes_lod=self.db_table_aircraft.attributes)
        self.comboboxentry_aircraft_id.populate(aircraft_on_ground_lod)
        self.action = "tow"


    def setup_landing(self):
        self.show()
        self.window.set_title("Bitte landendes Flugzeug eingeben...")

        airbourne_aircraft_lod = self.db_table_aircraft.get_airbourne_aircraft()
        self.comboboxentry_aircraft_id.initialize(definition_dic={'column_name': ['aircraft_id', 'aircraft_pattern'], 'mask': '%(aircraft_id)s - %(aircraft_pattern)s'},
                                                  attributes_lod=self.db_table_aircraft.attributes)
        self.comboboxentry_aircraft_id.populate(airbourne_aircraft_lod)
        self.action = "landing"



class window_start_record:
    def __init__(self, db_object, ui_table):
        self.db_object = db_object
        self.ui_table = ui_table
        
        self.db_table_aircraft = aircraft.db_table_aircraft(self.db_object)
        
        # TODO: Could there be a way to define the Frames as Forms?
        self.form_start_definition = []
        
        #self.db_table_aircraft = db_table(DBcnx, 'aircraft')
        #self.db_table_members = db_table(DBcnx, 'members')
        #self.db_table_flight_types = db_table(DBcnx, 'flight_types')
        #self.db_table_flight_types_aircraft = db_table(DBcnx, 'flight_types_aircraft')
        #self.db_table_flight_record = db_table(DBcnx, 'flight_record')
        #self.db_table_start_charges = db_table(DBcnx, 'start_charges')
        #self.db_table_charge_templates = db_table(DBcnx, "charge_templates")

        #self.portlet_table = portlet_table
        #self.comboboxentry_flight_type_content = []


# Window creation and handling --------------------------------------------
    def show(self):
        self.wTree = Glade.import_tree(self, RESOURCE_DIR + 'forms.glade', 'window_start_record')
        self.window = self.wTree.get_widget("window_start_record")
        
        self.button_start = self.wTree.get_widget("button_start")
        self.button_start.set_sensitive(1)

        self.entry_time = Entrys.Simple(self.wTree.get_widget("entry_time"))
        self.entry_date = Entrys.Simple(self.wTree.get_widget("entry_date"))
        self.set_time_entry()

        self.vbox_payment_info = self.wTree.get_widget("vbox_payment_info")
        self.button_payment_info = self.wTree.get_widget("button_payment_info")

        self.frame_start = self.wTree.get_widget("frame_start")
        self.entry_starting_location = Entrys.Simple(self.wTree.get_widget("entry_starting_location"))
        self.comboboxentry_flight_type = Entrys.Combobox(self.wTree.get_widget('comboboxentry_flight_type'))

        self.frame_aircraft = self.wTree.get_widget("frame_aircraft")
        self.entry_aircraft_id = self.wTree.get_widget("entry_aircraft_id")
        self.entry_aircraft_pattern = self.wTree.get_widget("entry_aircraft_pattern")
        self.comboboxentry_aircraft_pilot = self.wTree.get_widget("comboboxentry_aircraft_pilot")
        self.comboboxentry_aircraft_companion = self.wTree.get_widget("comboboxentry_aircraft_companion")
        self.label_aircraft_companion = self.wTree.get_widget("label_aircraft_companion")
        self.entry_counter_start = self.wTree.get_widget("entry_counter_start")
        self.label_counter_start = self.wTree.get_widget("label_counter_start")

        self.frame_sailplane = self.wTree.get_widget("frame_sailplane")
        self.entry_sailplane_id = self.wTree.get_widget("entry_sailplane_id")
        self.entry_sailplane_pattern = self.wTree.get_widget("entry_sailplane_pattern")
        self.comboboxentry_sailplane_pilot = self.wTree.get_widget("comboboxentry_sailplane_pilot")
        self.comboboxentry_sailplane_companion = self.wTree.get_widget("comboboxentry_sailplane_companion")
        self.label_sailplane_companion = self.wTree.get_widget("label_sailplane_companion")

        self.frame_payment_info = self.wTree.get_widget("frame_payment_info")
        self.comboboxentry_alternative_payer = self.wTree.get_widget("comboboxentry_alternative_payer")
        self.populate_frame_payment_info()

        self.payment_info_open = False
        self.available_personal_list = self.get_full_personal_list()
        gobject.timeout_add(1000, self.set_time_entry)
        
        
    # Widget signals ----------------------------------------------------------
    def on_button_start_clicked(self, widget=None):
        key_number = self.db_table_flight_record.get_first_key_number()

        start_record_dict = {}
        start_record_dict["pk_key_number"] = key_number

        start_record_dict["fk_flight_type"] = get_comboboxentry_selection(self.comboboxentry_flight_type)[0]
        start_record_dict["starting_location"] = self.entry_starting_location.get_text()
        start_record_dict["starting_type"] = self.start_type
        start_record_dict["starting_date"] = convert_gmdate_to_usdate(self.entry_date.get_text())
        start_record_dict["starting_time"] = self.entry_time.get_text()

        start_record_dict["alternative_payer"] = self.comboboxentry_alternative_payer.child.get_text()
        #start_record_dict["coupon_numbers"] = ""
        #start_record_dict["cash_payment"] = ""

        try:
            counter_start = float(self.entry_counter_start.get_text())
            start_record_dict["counter_start"] = counter_start
        except Exception, inst:
            if DEBUG: print inst

        # Start Sailplane
        if self.start_type == "winch" or self.start_type == "tow":
            sailplane_id = self.entry_sailplane_id.get_text()
            self.set_aircraft_airborne(self.fk_sailplane)

            #if self.start_type == "tow":
                #start_record_dict['fk_connected_record'] = self.fk_aircraft

            start_record_dict["fk_aircraft"] = self.fk_sailplane
            start_record_dict["fk_pilot"] = get_comboboxentry_selection(self.comboboxentry_sailplane_pilot)[0] #.child.get_text()

            aircraft_companion = get_comboboxentry_selection(self.comboboxentry_sailplane_companion)[0]
            if aircraft_companion <> ():
                start_record_dict["fk_companion"] = aircraft_companion
            self.db_table_flight_record.insert_data(db_table_layout_list=None, content_dict=start_record_dict)

        # Start Aircraft
        if self.start_type == "self" or self.start_type == "tow":
            self.set_aircraft_airborne(self.fk_aircraft)

            if self.start_type == "tow":
                tow_key_number = self.db_table_flight_record.get_first_key_number()
                start_record_dict["pk_key_number"] = tow_key_number
                start_record_dict["fk_flight_type"] = 0
                start_record_dict['fk_connected_record'] = key_number

                sailplane_record_dict = {}
                sailplane_record_dict['fk_connected_record'] = tow_key_number
                self.db_table_flight_record.update_data(key_number, content_dict=sailplane_record_dict)

            start_record_dict["fk_aircraft"] = self.fk_aircraft
            start_record_dict["fk_pilot"] = get_comboboxentry_selection(self.comboboxentry_aircraft_pilot)[0] #.child.get_text()

            aircraft_companion = get_comboboxentry_selection(self.comboboxentry_aircraft_companion)[0]
            if aircraft_companion <> ():
                start_record_dict["fk_companion"] = aircraft_companion
            self.db_table_flight_record.insert_data(db_table_layout_list=None, content_dict=start_record_dict)

        self.portlet_table.update_table_portlet()
        self.window.destroy()


    def on_button_cancel_clicked(self, widget=None):
        self.window.destroy()


    def on_button_payment_info_clicked(self, widget=None):
        alignment = widget.get_children()[0]
        hbox = alignment.get_children()[0]
        image, label = hbox.get_children()

        if self.payment_info_open == False:
            self.vbox_payment_info.show()
            image.set_from_stock(gtk.STOCK_GOTO_FIRST, gtk.ICON_SIZE_BUTTON)
        else:
            self.vbox_payment_info.hide()
            image.set_from_stock(gtk.STOCK_GOTO_LAST, gtk.ICON_SIZE_BUTTON)

        self.payment_info_open = not self.payment_info_open


    def on_entry_changed(self, widget=None):
        start_record_valid = True

        # Handle Personal comboboxentrys --------------------------------------
        full_personal_list = self.get_full_personal_list()

        comboboxentry_list = []
        comboboxentry_list.append(self.comboboxentry_aircraft_pilot)
        comboboxentry_list.append(self.comboboxentry_aircraft_companion)
        comboboxentry_list.append(self.comboboxentry_sailplane_pilot)
        comboboxentry_list.append(self.comboboxentry_sailplane_companion)

        selection_list = []
        for comboboxentry in comboboxentry_list:
            selection_list.append(get_comboboxentry_selection(comboboxentry))

        for comboboxentry in comboboxentry_list:
            if get_comboboxentry_selection(comboboxentry) <> [()]:
                if selection_list.count(get_comboboxentry_selection(comboboxentry)) > 1:
                    set_red(comboboxentry.child)
                    start_record_valid = False
                else:
                    set_white(comboboxentry.child)

        if self.start_type == "tow" or self.start_type == "self":
            if get_comboboxentry_selection(comboboxentry_list[0]) == [()]:
                start_record_valid = False
                set_red(comboboxentry_list[0].child)
        if self.start_type == "tow" or self.start_type == "winch":
            if get_comboboxentry_selection(comboboxentry_list[2]) == [()]:
                start_record_valid = False
                set_red(comboboxentry_list[2].child)

        # Handle flight types combobox ----------------------------------------
        flight_type = self.comboboxentry_flight_type.child.get_text()
        flight_type_list = []
        for entry in self.comboboxentry_flight_type_content:
            flight_type_list.append(unicode(entry[1], "latin-1"))
        if flight_type not in flight_type_list:
            set_red(self.comboboxentry_flight_type.child)
            start_record_valid = False
        else:
            set_white(self.comboboxentry_flight_type.child)

        if start_record_valid:
            self.button_start.set_sensitive(1)
        else:
            self.button_start.set_sensitive(0)


    # main functions ----------------------------------------------------------
    def set_aircraft_airborne(self, fk_aircraft):
        #aircraft_key_number = self.db_table_aircraft.search_column("aircraft_id", aircraft_id, "pk_key_number")[0]
        aircraft_dict = {}
        aircraft_dict["pk_key_number"] = fk_aircraft
        aircraft_dict["airborne"] = "t"
        self.db_table_aircraft.update_data(fk_aircraft, content_dict=aircraft_dict)
        return


    def setup_self_start(self, aircraft_dic):
        self.start_type = "self"
        self.populate_frame_aircraft(aircraft_dic)
        self.populate_frame_start(aircraft_dic, None)
        self.window.show()


    def setup_winch_start(self, sailplane_dic):
        self.start_type = "winch"
        self.populate_frame_sailplane(sailplane_dic)
        self.populate_frame_start(None, sailplane_dic)
        self.window.show()


    def setup_tow_start(self, aircraft_dic, sailplane_dic):
        self.start_type = "tow"
        self.populate_frame_aircraft(aircraft_dic)
        self.populate_frame_sailplane(sailplane_dic)
        self.populate_frame_start(aircraft_dic, sailplane_dic)
        self.window.show()


    def set_time_entry(self):
        gmtime = time.strftime('%H:%M:%S', time.gmtime())
        gmdate = time.strftime('%d.%m.%Y', time.gmtime())

        self.entry_time.set_text(gmtime)
        self.entry_date.set_text(gmdate)
        return True


    def get_full_personal_list(self):
        full_personal_list = []
        #members_pk_list = self.db_table_members.get_column('pk_key_number') #get_available_personal_list("firstname", "lastname")
        #for pk_member in members_pk_list:
        #    member_name = self.db_table_members.search_column('pk_key_number', pk_member, 'show_as')[0]
        #    full_personal_list.append([pk_member, member_name])
        return full_personal_list


    # populating frames -------------------------------------------------------
    def populate_frame_start(self, aircraft_dic, sailplane_dic=None):
        print 'populate_frame_start with:'
        print '... aircraft :', aircraft_dic
        print '... sailplane:', sailplane_dic
        
        self.entry_starting_location.set_text("Seckendorf")
        if sailplane_dic <> None:
            print self.db_table_aircraft.get_allowed_flight_types(sailplane_dic['id'])
        #    matching_flight_types_key_list = self.db_table_flight_types_aircraft.search_column("fk_aircraft_key_number", fk_sailplane, "fk_allowed_flight_type_abbrevation")
        #else:
        #    matching_flight_types_key_list = self.db_table_flight_types_aircraft.search_column("fk_aircraft_key_number", fk_aircraft, "fk_allowed_flight_type_abbrevation")

        #matching_flight_types_list = []
        #if matching_flight_types_key_list <> [()]:
        #    for fk_flight_types in matching_flight_types_key_list:
        #        flight_type_abbrevation = self.db_table_flight_types.search_column("pk_key_number", fk_flight_types, "abbrevation")[0]
        #        flight_type_note = self.db_table_flight_types.search_column("pk_key_number", fk_flight_types, "note")[0]
        #        self.comboboxentry_flight_type_content.append([fk_flight_types, flight_type_abbrevation + " - " + flight_type_note])
        #else:
        #    dialog("Fehler", parent=self.window, label_text="""\
#Bitte definieren sie mindestens eine gültige
#Flugart für dieses Flugzeug!

#Die Flugarten werden benötigt, um den Flug
#abrechnen zu können. Sollten Sie keine Abrechnung
#wünschen, so legen Sie einfach eine Flugart ohne
#die Angabe eines Zahlers an und tragen diese dann
#unter "Flugzeuge" als gültig ein.""", dialog_type="error")
 #           self.window.destroy()
            #return

       # populate_comboboxentry_from_list(self.comboboxentry_flight_type, self.comboboxentry_flight_type_content, key_column=True)

       # if DEBUG: print "IDs:", fk_aircraft, fk_sailplane
   

    def populate_frame_aircraft(self, aircraft_dic):
        #aircraft_id = self.db_table_aircraft.search_column("pk_key_number", fk_aircraft, "aircraft_id")[0]

        self.frame_aircraft.show()
        #self.entry_aircraft_id.set_text(unicode(aircraft_id, "latin-1"))

        #aircraft_seats = self.db_table_aircraft.search_column("pk_key_number", fk_aircraft, "aircraft_seats")[0]
        #populate_comboboxentry_from_list(self.comboboxentry_aircraft_pilot, self.get_full_personal_list(), key_column=True)
        #if aircraft_seats > 1:
        #    populate_comboboxentry_from_list(self.comboboxentry_aircraft_companion, self.get_full_personal_list(), key_column=True)
        #else:
        #    self.comboboxentry_aircraft_companion.hide()
        #    self.label_aircraft_companion.hide()

        #runtime_counter = self.db_table_aircraft.search_column("pk_key_number", fk_aircraft, "runtime_counter")[0]
        #if runtime_counter == "t":
        ##    self.entry_counter_start.show()
         #   self.label_counter_start.show()

        #aircraft_pattern_list = self.db_table_aircraft.search_column("aircraft_id", aircraft_id, "aircraft_pattern")
        #self.entry_aircraft_pattern.set_text(unicode(aircraft_pattern_list[0], "latin-1"))
        #self.fk_aircraft = fk_aircraft
        return


    def populate_frame_sailplane(self, sailplane_dic):
        #sailplane_id = self.db_table_aircraft.search_column("pk_key_number", fk_sailplane, "aircraft_id")[0]

        self.frame_sailplane.show()
        #self.entry_sailplane_id.set_text(unicode(sailplane_id, "latin-1"))

        #aircraft_seats = self.db_table_aircraft.search_column("pk_key_number", fk_sailplane, "aircraft_seats")[0]
        #populate_comboboxentry_from_list(self.comboboxentry_sailplane_pilot, self.get_full_personal_list(), key_column=True)

#        if aircraft_seats > 1:
 #           populate_comboboxentry_from_list(self.comboboxentry_sailplane_companion, self.get_full_personal_list(), key_column=True)
  #      else:
   #         self.comboboxentry_sailplane_companion.hide()
#            self.label_sailplane_companion.hide()

 #       sailplane_pattern_list = self.db_table_aircraft.search_column("pk_key_number", fk_sailplane, "aircraft_pattern")
  #      self.entry_sailplane_pattern.set_text(unicode(sailplane_pattern_list[0], "latin-1"))
   #     self.fk_sailplane = fk_sailplane
        return


    def populate_frame_payment_info(self):
        #populate_comboboxentry_from_list(self.comboboxentry_aircraft_pilot, self.get_full_personal_list(), key_column=True)
        pass
    



class window_landing_record:
    def __init__(self, db_object, ui_table):
        self.db_object = db_object
        #self.db_table_flight_record = db_table(DBcnx, 'flight_record')
        #self.db_table_aircraft = db_table(DBcnx, 'aircraft')
        #self.db_table_landing_charges = db_table(DBcnx, 'landing_charges')
        #self.db_table_charge_templates = db_table(DBcnx, 'charge_templates')
        #self.db_table_members = db_table(DBcnx, 'members')
        #self.db_table_flight_types = db_table(DBcnx, 'flight_types')

        #self.class_charge = charges.charge(DBcnx)
        #self.portlet_table = portlet_table


    # Widget signals ----------------------------------------------------------
    def on_button_clicked(self, widget=None):
        button_label = widget.get_label()

        if button_label == "_Landung":
            widget.set_label("_Ok")
            self.set_button_touch_and_go(self.button_list[1])
            return

        if button_label == "_Ok":
            self.write_landing_record()

            aircraft_id = self.entry_aircraft_id.get_text()
            self.set_aircraft_grounded(aircraft_id)
            self.portlet_table.update_table_portlet()

        if button_label == "_Touch and Go":
            self.write_landing_record()
            self.write_starting_record()

            self.portlet_table.update_table_portlet()

        if button_label == "_Abbruch":
            if DEBUG: print "Abbruch"

        self.window.destroy()


    # main functions ----------------------------------------------------------
    def setup_landing(self, pk_aircraft):
        self.populate_frame_start(pk_aircraft)
        self.populate_frame_aircraft(pk_aircraft)
        self.populate_frame_landing()


    def write_landing_record(self):
        flight_record_result = self.db_table_flight_record.filter("pk_key_number = " + str(self.key_number))[0]

        fk_flight_type = flight_record_result['fk_flight_type']
        fk_aircraft = flight_record_result['fk_aircraft']
        fk_aircraft_charge = self.db_table_aircraft.search_column("pk_key_number", fk_aircraft, "fk_aircraft_charge")[0]

        if flight_record_result['starting_type'] == "self":
            modality = 1
        if flight_record_result['starting_type'] == "winch":
            modality = 2
        if flight_record_result['starting_type'] == "tow":
            modality = 3

        #print "...fk_aircraft_charge", fk_aircraft_charge, "modality", modality, "fk_flight_type", fk_flight_type
        pk_charge_template = self.class_charge.get_charge_template(pk_charge=fk_aircraft_charge, booking_modality=modality, pk_flight_type=fk_flight_type, start=False, landing=True)
        #print "   pk_charge_template:", pk_charge_template

        flight_time = 0
        motor_runtime = 0
        tow_altitude = 0

        landing_charge = self.class_charge.calculate_from_template(pk_charge_template, flight_time, motor_runtime, tow_altitude)

        landing_record_dict = {}
        landing_record_dict["pk_key_number"] = self.key_number
        landing_record_dict["landing_time"] = self.entry_landing_time.get_text()
        landing_record_dict["landing_date"] = convert_gmdate_to_usdate(self.entry_landing_date.get_text())
        landing_record_dict["landing_location"] = self.entry_landing_location.get_text()
        landing_record_dict["landing_charge"] = landing_charge

        try:
            counter_landing = float(self.entry_counter_landing.get_text())
            landing_record_dict["counter_landing"] = counter_landing
        except Exception, inst:
            if DEBUG: print inst

        self.db_table_flight_record.update_data(self.key_number, content_dict=landing_record_dict)


    def write_starting_record(self):
        class_window_flight_record = window_flight_record(self.DBcnx, self)
        db_table_layout_flight_record = class_window_flight_record.db_table_layout

        starting_record_dict = {}
        starting_record_dict["pk_key_number"] = self.db_table_flight_record.get_first_key_number()
        starting_record_dict["fk_aircraft"] = self.db_table_flight_record.search_column('pk_key_number', self.key_number, 'fk_aircraft')[0] #self.entry_aircraft_id.get_text()
        starting_record_dict["fk_flight_type"] = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "fk_flight_type")[0]

        starting_record_dict["starting_location"] = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "starting_location")[0]
        starting_record_dict["starting_type"] = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "starting_type")[0]
        starting_record_dict["starting_date"] = convert_gmdate_to_usdate(self.entry_landing_date.get_text())
        starting_record_dict["starting_time"] = self.entry_landing_time.get_text()

        starting_record_dict["fk_pilot"] = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "fk_pilot")[0]
        starting_record_dict["fk_companion"] = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "fk_companion")[0]

        starting_record_dict["fk_alternative_payer"] = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "fk_alternative_payer")[0]
        starting_record_dict["coupon_numbers"] = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "coupon_numbers")[0]
        starting_record_dict["cash_payment"] = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "cash_payment")[0]
        self.db_table_flight_record.insert_data(db_table_layout_flight_record, starting_record_dict)
        return


    def set_aircraft_grounded(self, aircraft_id):
        aircraft_key_number = self.db_table_aircraft.search_column("aircraft_id", aircraft_id, "pk_key_number")[0]
        aircraft_dict = {}
        aircraft_dict["pk_key_number"] = aircraft_key_number
        aircraft_dict["airborne"] = "f"
        self.db_table_aircraft.update_data(aircraft_key_number, content_dict=aircraft_dict)
        return


    # populating frames -------------------------------------------------------
    def populate_frame_start(self, pk_aircraft):
        # Look for dataset with empty landing_time and matching pk_aircraft
        flight_records_without_landing = self.db_table_flight_record.filter('fk_aircraft = ' + str(pk_aircraft) + ' AND landing_time IS NULL')
        for flight_record in flight_records_without_landing:
            self.key_number = flight_record['pk_key_number']

        starting_time = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "starting_time")[0]
        self.entry_start_time.set_text(starting_time)
        starting_date = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "starting_date")[0]
        starting_date = starting_date[8:10] + "." + starting_date[5:7] + "." + starting_date[0:4]
        self.entry_start_date.set_text(starting_date)
        starting_location = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "starting_location")[0]
        self.entry_start_location.set_text(starting_location)


    def populate_frame_aircraft(self, pk_aircraft):
        aircraft_id = self.db_table_aircraft.search_column('pk_key_number', pk_aircraft, 'aircraft_id')[0]

        # Get motorruntime_counter need
        runtime_counter = self.db_table_aircraft.search_column("pk_key_number", pk_aircraft, "runtime_counter")[0]
        print "runtime_counter:", runtime_counter
        if runtime_counter == "t":
            counter_start = self.db_table_flight_record.search_column("pk_key_number", self.key_number, "counter_start")[0]
            if counter_start <> "":
                self.entry_counter_landing.show()
                self.label_counter_landing.show()

        self.entry_aircraft_id.set_text(aircraft_id)
        aircraft_pattern = self.db_table_aircraft.search_column("pk_key_number", pk_aircraft, "aircraft_pattern")[0]
        self.entry_aircraft_pattern.set_text(unicode(aircraft_pattern, "latin-1"))

        self.entry_flight_type.set_text(self.db_table_flight_record.get_foreign_cell_text(self.key_number, 'fk_flight_type', self.db_table_flight_types, 'abbrevation'))
        self.entry_aircraft_pilot.set_text(self.db_table_flight_record.get_foreign_cell_text(self.key_number, 'fk_pilot', self.db_table_members, 'show_as'))
        self.entry_aircraft_companion.set_text(self.db_table_flight_record.get_foreign_cell_text(self.key_number, 'fk_companion', self.db_table_members, 'show_as'))

        if DEBUG: print "landing aircraft", aircraft_id, self.key_number


    def populate_frame_landing(self):
        self.entry_landing_location.set_text("Seckendorf")

        # Just show the tow_altitude combobox, if the plane was towed!
        starting_type = self.db_table_flight_record.search_column('pk_key_number', self.key_number, 'starting_type')[0]
        if starting_type == "tow":
            self.label_tow_altitude.show()
            self.comboboxentry_tow_altitude.show()


    def set_button_touch_and_go(self, button):
        # TODO: Make this dependent on primary key flight record!
        aircraft_id = self.entry_aircraft_id.get_text()
        self_start_capable = self.db_table_aircraft.search_column("aircraft_id", aircraft_id, "self_start")
        if self_start_capable[0] == "t":
            self.button_list[1].set_sensitive(1)
        else:
            self.button_list[1].set_sensitive(0)
        return


    def set_time_entry(self):
        gmtime_string = get_gmtime_str()
        gmdate_string = get_gmdate_str()
        self.entry_landing_time.set_text(gmtime_string)
        self.entry_landing_date.set_text(gmdate_string)

        start_time_string = self.entry_start_time.get_text()
        start_date_string = self.entry_start_date.get_text()
        datetime_delta_string = get_gmdatetime_deltastring(start_date_string, start_time_string, gmdate_string, gmtime_string)

        self.entry_flight_time.set_text(datetime_delta_string)
        return True


    # Window creation and handling --------------------------------------------
    def initGUIwindow(self, nowindow=False):
        self.wTree = import_glade_tree(self, "forms.glade", "window_landing_record")
        self.window = self.wTree.get_widget("window_landing_record")
        self.window.set_keep_above(True)

        self.entry_start_time = self.wTree.get_widget("entry_start_time")
        self.entry_start_date = self.wTree.get_widget("entry_start_date")
        self.entry_start_location = self.wTree.get_widget("entry_start_location")
        # ---------------------------------------------------------------------
        self.entry_aircraft_id = self.wTree.get_widget("entry_aircraft_id")
        self.entry_aircraft_pattern = self.wTree.get_widget("entry_aircraft_pattern")
        self.entry_flight_type = self.wTree.get_widget("entry_flight_type")
        self.entry_aircraft_pilot = self.wTree.get_widget("entry_aircraft_pilot")
        self.entry_aircraft_companion = self.wTree.get_widget("entry_aircraft_companion")
        # ---------------------------------------------------------------------
        self.entry_landing_time = self.wTree.get_widget("entry_landing_time")
        self.entry_landing_date = self.wTree.get_widget("entry_landing_date")
        self.entry_landing_location = self.wTree.get_widget("entry_landing_location")
        self.entry_flight_time = self.wTree.get_widget("entry_flight_time")
        self.label_tow_altitude = self.wTree.get_widget("label_tow_altitude")
        self.comboboxentry_tow_altitude = self.wTree.get_widget("comboboxentry_tow_altitude")
        self.entry_counter_landing = self.wTree.get_widget("entry_counter_landing")
        self.label_counter_landing = self.wTree.get_widget("label_counter_landing")
        self.set_time_entry()

        self.button_list = []
        self.button_list.append(self.wTree.get_widget("button_1"))
        self.button_list.append(self.wTree.get_widget("button_2"))
        self.button_list.append(self.wTree.get_widget("button_3"))

        self.button_list[0].set_label("_Landung")
        self.button_list[1].set_label("_Touch and Go")
        self.button_list[1].set_sensitive(0)
        self.button_list[2].set_label("_Abbruch")

        if nowindow == True:
            self.portlet = self.window.get_child()
            self.window.remove(self.portlet)
            self.window.destroy()
            return self.portlet

        gobject.timeout_add(1000, self.set_time_entry)



#class window_flight_record:
    # TODO: This record should be separated in fk_towplane, fk_towed_plane_1, fk_towed_plane_2 because of double-tow-ability.

#    def __init__(self, database, table_portlet):
#        self.database = database
#        self.table_portlet = table_portlet


    # Database layout ---------------------------------------------------------
    #def db_table_layout(self):
    #    db_table_layout_list = []

    #    db_table_layout_list.append({'db_field_name': 'pk_key_number'    , 'db_field_type': 'bigint'      , 'gtk_widget_name': 'entry_key_number'         , 'gtk_treeview_column':  0, 'print_table_column': None, 'db_primary_key': True, 'gtk_column_hide': True})

    #    db_table_layout_list.append({'db_field_name': 'starting_location', 'db_field_type': 'varchar (40)', 'gtk_widget_name': 'entry_starting_location'  , 'gtk_treeview_column':  1, 'print_table_column':  1, 'column_title': 'Startort', 'gtk_column_hide': True})
    #    db_table_layout_list.append({'db_field_name': 'starting_type'    , 'db_field_type': 'varchar (40)', 'gtk_widget_name': 'entry_starting_type'      , 'gtk_treeview_column':  2, 'print_table_column':  2, 'column_title': 'Startart', 'gtk_column_hide': True})
    #    db_table_layout_list.append({'db_field_name': 'starting_date'    , 'db_field_type': 'date'        , 'gtk_widget_name': 'entry_starting_date'      , 'gtk_treeview_column':  3, 'print_table_column':  3, 'column_title': 'Startdatum'})
    #    db_table_layout_list.append({'db_field_name': 'starting_time'    , 'db_field_type': 'time'        , 'gtk_widget_name': 'entry_starting_time'      , 'gtk_treeview_column':  4, 'print_table_column':  4, 'column_title': 'Startzeit'})

    #    db_table_layout_list.append({'db_field_name': 'landing_location' , 'db_field_type': 'varchar (40)', 'gtk_widget_name': 'entry_landing_location'   , 'gtk_treeview_column': 10, 'print_table_column': 10, 'column_title': 'Landeort'})
    #    db_table_layout_list.append({'db_field_name': 'landing_type'     , 'db_field_type': 'varchar (40)', 'gtk_widget_name': 'entry_landing_type'       , 'gtk_treeview_column': 11, 'print_table_column': 11, 'column_title': 'Landeart', 'gtk_column_hide': True})
    #    db_table_layout_list.append({'db_field_name': 'landing_date'     , 'db_field_type': 'date'        , 'gtk_widget_name': 'entry_landing_date'       , 'gtk_treeview_column': 12, 'print_table_column': 12, 'column_title': 'Landedatum'})
    #    db_table_layout_list.append({'db_field_name': 'landing_time'     , 'db_field_type': 'time'        , 'gtk_widget_name': 'entry_landing_time'       , 'gtk_treeview_column': 13, 'print_table_column': 13, 'column_title': 'Landezeit'})

    #    db_table_layout_list.append({'db_field_name': 'tow_altitude'     , 'db_field_type': 'integer'     , 'gtk_widget_name': 'comboboxentry_tow_altitude', 'gtk_treeview_column': 15, 'print_table_column': 15, 'column_title': 'Schlepphöhe',         'gtk_column_hide': True})
    #    db_table_layout_list.append({'db_field_name': 'counter_start'    , 'db_field_type': 'float'       , 'gtk_widget_name': 'entry_counter_start'       , 'gtk_treeview_column': 16, 'print_table_column': 16, 'column_title': 'Zählerstand Start',   'gtk_column_hide': True})
    #    db_table_layout_list.append({'db_field_name': 'counter_landing'  , 'db_field_type': 'float'       , 'gtk_widget_name': 'entry_counter_landing'     , 'gtk_treeview_column': 17, 'print_table_column': 17, 'column_title': 'Zählerstand Landung', 'gtk_column_hide': True})

    #    db_table_layout_list.append({'db_field_name': 'start_charge'   , 'db_field_type': 'float'         , 'gtk_treeview_column':   21, 'print_table_column':  18, 'column_title': 'Startgebühr'})
    #    db_table_layout_list.append({'db_field_name': 'landing_charge' , 'db_field_type': 'float'         , 'gtk_treeview_column':   22, 'print_table_column':  19, 'column_title': 'Landegebühr'})

    #    db_table_layout_list.append({'db_field_name': 'fk_aircraft'         , 'gtk_widget_name': 'comboboxentry_aircraft_id'       , 'db_foreign_table': 'aircraft'     , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'aircraft_id'  , 'gtk_treeview_column':  7, 'column_title': 'Kennzeichen'})

        # TODO: This record should be separated in fk_towplane, fk_towed_plane_1, fk_towed_plane_2 because of double-tow-ability.
    #    db_table_layout_list.append({'db_field_name': 'fk_connected_record' , 'gtk_widget_name': 'comboboxentry_connected_record'  , 'db_foreign_table': 'flight_record', 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'pk_key_number', 'gtk_treeview_column':  6, 'column_title': 'Verbunden mit', 'gtk_column_hide': False})

    #    db_table_layout_list.append({'db_field_name': 'fk_flight_type'      , 'gtk_widget_name': 'comboboxentry_flight_type'       , 'db_foreign_table': 'flight_types' , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'abbrevation'  , 'gtk_treeview_column':  5, 'column_title': 'Flugart'})
    #    db_table_layout_list.append({'db_field_name': 'fk_pilot'            , 'gtk_widget_name': 'comboboxentry_aircraft_pilot'    , 'db_foreign_table': 'members'      , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'show_as'      , 'gtk_treeview_column':  8, 'column_title': 'Pilot'})
    #    db_table_layout_list.append({'db_field_name': 'fk_companion'        , 'gtk_widget_name': 'comboboxentry_aircraft_companion', 'db_foreign_table': 'members'      , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'show_as'      , 'gtk_treeview_column':  9, 'column_title': 'Begleiter'})
    #    db_table_layout_list.append({'db_field_name': 'fk_alternative_payer', 'gtk_widget_name': 'comboboxentry_alternative_payer' , 'db_foreign_table': 'members'      , 'db_foreign_key_column': 'pk_key_number', 'db_foreign_field_name': 'show_as'      , 'gtk_treeview_column': 14, 'column_title': 'Zahler'})
        #db_table_layout_list.append({'db_field_name': 'coupon_numbers'      , 'db_field_type': 'varchar (40)'   , 'gtk_widget_name': 'entry_coupon_numbers', 'gtk_treeview_column':   10, 'print_table_column':  10})
        #db_table_layout_list.append({'db_field_name': 'cash_payment'        , 'db_field_type': 'money'          , 'gtk_widget_name': 'entry_cash_payment'  , 'gtk_treeview_column':   10, 'print_table_column':  10})
    #    return db_table_layout_list



class reports:
    def __init__(self, database, report_exporter):
        self.database = database
        self.report_exporter_main = report_exporter

        self.db_table_flight_recording = db_table(self.database)
        self.db_table_flight_types = SQLdb.table(self.database, "flight_types")
        self.db_table_person = SQLdb.table(self.database, "person")
        self.db_table_aircraft = SQLdb.table(self.database, "aircraft")


    def menu_layout(self):
        treeview_functions = []
        treeview_functions.append([gtk.gdk.pixbuf_new_from_file(RESOURCE_DIR + "report_32.png"), unicode ("Hauptflugbuch", "latin-1"), 0])
        treeview_functions.append([gtk.gdk.pixbuf_new_from_file(RESOURCE_DIR + "report_32.png"), unicode ("Gebührenübersicht", "latin-1"), 0])
        treeview_functions.append([gtk.gdk.pixbuf_new_from_file(RESOURCE_DIR + "report_32.png"), unicode ("Bordbuchzeiten", "latin-1"), 0])
        treeview_functions.append([gtk.gdk.pixbuf_new_from_file(RESOURCE_DIR + "report_32.png"), unicode ("Zeiten für Schlepppiloten", "latin-1"), 0])
        treeview_functions.append([gtk.gdk.pixbuf_new_from_file(RESOURCE_DIR + "report_32.png"), unicode ("Ausbildung", "latin-1"), 0])
        return treeview_functions


    def show_menu(self):
        self.report_exporter_main.initGUIportlet(self.menu_layout())
        self.report_exporter_main.append_function_on_selection(self.main_flight_book, 'Hauptflugbuch')
        self.report_exporter_main.append_function_on_selection(self.charge_overview, 'Gebührenübersicht')
        self.report_exporter_main.append_function_on_selection(self.bord_book, 'Bordbuchzeiten')
        self.report_exporter_main.append_function_on_selection(self.tow_times, 'Zeiten für Schlepppiloten')
        self.report_exporter_main.append_function_on_selection(self.training, 'Ausbildung')


    # Here are the reports for this module ------------------------------------
    def main_flight_book(self, from_date=None, to_date=None, filename=None):
        table_name = "Hauptflugbuch"
        table_flight_recording_content = self.db_table_flight_recording.select()

        # open HTML table -----------------------------------------------------
        HTML_body = """\
        <h2>""" + table_name + """</h2>

        <div>Zeitraum von """ + from_date + " bis " + to_date + """\
        </div>

        <br>

        <table>
            <thead>
                <tr>
                    <th>Nummer</th>
                    <th>Flugart</th>
                    <th>Startzeit</th>
                    <th colspan=5>Startort</th>
                </tr>
                <tr>
                    <th>Kennzeichen</th>
                    <th>Muster</th>
                    <th>Landezeit</th>
                    <th>Landeort</th>
                    <th>Pilot</th>
                    <th>Begleiter</th>
                    <th>Dauer</th>
                </tr>
            </thead>
"""

        HTML_body += """\
            <tbody>
"""

        odd_offset = True
        for row in table_flight_recording_content:
            flight_type_abbrevation = self.db_table_flight_types.search_column("pk_key_number", row['fk_flight_type'], "abbrevation")[0]
            pilot_name = self.db_table_members.search_column("pk_key_number", row['fk_pilot'], "show_as")[0]
            companion_name = self.db_table_members.search_column("pk_key_number", row['fk_companion'], "show_as")[0]
            aircraft_id = self.db_table_aircraft.search_column("pk_key_number", row['fk_aircraft'], "aircraft_id")[0]
            aircraft_pattern = self.db_table_aircraft.search_column("pk_key_number", row['fk_aircraft'], "aircraft_pattern")[0]

            # Get timedelta if times and dates are correctly given. If not landed, set timedelta to zero.
            starting_date, starting_time = convert_usdate_to_gmdate(row['starting_date']), row['starting_time']
            landing_date, landing_time =   convert_usdate_to_gmdate(row['landing_date']), row['landing_time']

            if starting_date <> None and landing_date <> None and starting_time <> None and landing_time <> None:
                datetime_delta_string = get_gmdatetime_deltastring(starting_date, starting_time, landing_date, landing_time)
            else:
                datetime_delta_string = "-"

            if companion_name == (): companion_name = "-"

            if odd_offset:
                HTML_body += """\
                <tr class="zebrastreifen_ungerade">
"""
            else:
                HTML_body += """\
                <tr class="zebrastreifen_gerade">
"""

            HTML_body += """\
                    <td>""" + str(row['pk_key_number']) + "</td>" + """
                    <td>""" + str(flight_type_abbrevation) + "</td>" + """
                    <td>""" + str(row['starting_time']) + "</td>" + """
                    <td colspan=4>""" + str(row['starting_location']) + "</td>" + """
"""

            HTML_body += """\
                </tr>
"""
            if odd_offset:
                HTML_body += """\
                <tr class="zebrastreifen_ungerade">
"""
            else:
                HTML_body += """\
                <tr class="zebrastreifen_gerade">
"""
            HTML_body += """\
                    <td>""" + str(aircraft_id) + "</td>" + """
                    <td>""" + str(aircraft_pattern) + "</td>" + """
                    <td>""" + str(row['landing_time']) + "</td>" + """
                    <td>""" + str(row['landing_location']) + "</td>" + """
                    <td>""" + str(pilot_name) + "</td>" + """
                    <td>""" + str(companion_name) + "</td>" + """
                    <td>""" + datetime_delta_string + "</td>" + """
"""

            HTML_body += """\
                </tr>
"""
            odd_offset = not odd_offset

        # close HTML table ----------------------------------------------------
        HTML_body += """\
            </tbody>
        </table>
"""
        return table_name, HTML_body

    def charge_overview(self, from_date=None, to_date=None, filename=None):
        table_name = "Gebührenübersicht"

        HTML_body = """\
        <h2>""" + table_name + """</h2>

        <table>
            <thead>
                <tr>
                    <th colspan=8>Zahler</th>
                </tr>
                <tr>
                    <th width=5%></th>
                    <th>Nummer</th>
                    <th>Flugart</th>
                    <th>Kennzeichen</th>
                    <th colspan=3>Pilot</th>
                    <th>Betrag</th>
                </tr>
                <tr>
                    <th width=5%></th>
                    <th colspan=2>Startzeit</th>
                    <th colspan=2>Startort</th>
                    <th>Landezeit</th>
                    <th>Landeort</th>
                    <th>Schl.Hö./Mot.Lz.</th>
                </tr>
            </thead>
            <tbody>
"""
        for z in xrange(0, 1000):
            for y in xrange(0,3):
                HTML_body += """\
                    <tr class="zebrastreifen_ungerade">
"""
                for x in xrange(0,8):
                    HTML_body += """\
                        <td>Chickedy china</td>
"""
                HTML_body += """\
                    </tr>
"""
        HTML_body += """\
            </tbody>
        </table>
"""
        return table_name, HTML_body

    def bord_book(self, from_date=None, to_date=None, filename=None):
        table_name = "Bordbuch-Zeiten"

        HTML_body = """\
        <h2>""" + table_name + """</h2>

        <table>
            <thead>
                <tr>
                    <th colspan=8>Zahler</th>
                </tr>
            </thead>
            <thead>
                <tr>
                    <th width=5%></th>
                    <th>Nummer</th>
                    <th>Flugart</th>
                    <th>Kennzeichen</th>
                    <th colspan=3>Pilot</th>
                    <th>Betrag</th>
                </tr>
            </thead>
            <thead>
                <tr>
                    <th width=5%></th>
                    <th colspan=2>Startzeit</th>
                    <th colspan=2>Startort</th>
                    <th>Landezeit</th>
                    <th>Landeort</th>
                    <th>Schl.Hö./Mot.Lz.</th>
                </tr>
            </thead>
        </table>
"""
        return table_name, HTML_body

    def training(self, from_date=None, to_date=None, filename=None):
        table_name = "Ausbildung"

        HTML_body = """\
        <h2>""" + table_name + """</h2>

        <table>
            <thead>
                <tr>
                    <th colspan=8>Zahler</th>
                </tr>
            </thead>
            <thead>
                <tr>
                    <th width=5%></th>
                    <th>Nummer</th>
                    <th>Flugart</th>
                    <th>Kennzeichen</th>
                    <th colspan=3>Pilot</th>
                    <th>Betrag</th>
                </tr>
            </thead>
            <thead>
                <tr>
                    <th width=5%></th>
                    <th colspan=2>Startzeit</th>
                    <th colspan=2>Startort</th>
                    <th>Landezeit</th>
                    <th>Landeort</th>
                    <th>Schl.Hö./Mot.Lz.</th>
                </tr>
            </thead>
        </table>
"""
        return table_name, HTML_body

    def tow_times(self, from_date=None, to_date=None, filename=None):
        table_name = "Zeiten für Schleppiloten"

        HTML_body = """\
        <h2>""" + table_name + """</h2>

        <table>
            <thead>
                <tr>
                    <th colspan=8>Zahler</th>
                </tr>
            </thead>
            <thead>
                <tr>
                    <th width=5%></th>
                    <th>Nummer</th>
                    <th>Flugart</th>
                    <th>Kennzeichen</th>
                    <th colspan=3>Pilot</th>
                    <th>Betrag</th>
                </tr>
            </thead>
            <thead>
                <tr>
                    <th width=5%></th>
                    <th colspan=2>Startzeit</th>
                    <th colspan=2>Startort</th>
                    <th>Landezeit</th>
                    <th>Landeort</th>
                    <th>Schl.Hö./Mot.Lz.</th>
                </tr>
            </thead>
        </table>
"""
        return table_name, HTML_body



class db_table(SQLdb.table):
    attributes = \
    [
        {'column_name': 'id',                   'data_type': 'bigint',  'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'starting_location',    'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'starting_type',        'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'starting_date',        'data_type': 'date'},
        {'column_name': 'starting_time',        'data_type': 'time'},
        {'column_name': 'landing_location',     'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'landing_type',         'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'landing_date',         'data_type': 'date'},
        {'column_name': 'landing_time',         'data_type': 'time'},
        {'column_name': 'tow_altitude',         'data_type': 'integer'},
        {'column_name': 'counter_start',        'data_type': 'float'},
        {'column_name': 'counter_landing',      'data_type': 'float'},
        {'column_name': 'start_charge',         'data_type': 'float'},
        {'column_name': 'landing_charge',       'data_type': 'float'},
        {'column_name': 'fk_aircraft',          'data_type': 'bigint', 'referenced_table_name': 'aircraft',    'referenced_column_name': 'id'},
        {'column_name': 'fk_towplane',          'data_type': 'bigint', 'referenced_table_name': 'aircraft',    'referenced_column_name': 'id'},
        {'column_name': 'fk_towed_plane_1',     'data_type': 'bigint', 'referenced_table_name': 'aircraft',    'referenced_column_name': 'id'},
        {'column_name': 'fk_towed_plane_2',     'data_type': 'bigint', 'referenced_table_name': 'aircraft',    'referenced_column_name': 'id'},
        {'column_name': 'fk_flight_type',       'data_type': 'bigint', 'referenced_table_name': 'flight_type', 'referenced_column_name': 'id'},
        {'column_name': 'fk_pilot',             'data_type': 'bigint', 'referenced_table_name': 'person',      'referenced_column_name': 'id'},
        {'column_name': 'fk_companion',         'data_type': 'bigint', 'referenced_table_name': 'person',      'referenced_column_name': 'id'},
        {'column_name': 'fk_alternative_payer', 'data_type': 'bigint', 'referenced_table_name': 'person',      'referenced_column_name': 'id'},
        {'column_name': 'created',              'data_type': 'timestamp'},
        {'column_name': 'updated',              'data_type': 'timestamp'},
        {'column_name': 'deactivated',          'data_type': 'bool'}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'flight_record')
        try:
            differences_lod = self.check_attributes(self.attributes, add=True)
        except:
            raise


class ui_form(Portlets.Form):
    definition = \
    [
        {'column_name': 'starting_location',    'widget_name': 'entry_starting_location'},
        {'column_name': 'starting_type',        'widget_name': 'entry_starting_type'},
        {'column_name': 'starting_date',        'widget_name': 'entry_starting_date'},
        {'column_name': 'starting_time',        'widget_name': 'entry_starting_time'},
        {'column_name': 'landing_location',     'widget_name': 'entry_landing_location'},
        {'column_name': 'landing_type',         'widget_name': 'entry_landing_type'},
        {'column_name': 'landing_date',         'widget_name': 'entry_landing_date'},
        {'column_name': 'landing_time',         'widget_name': 'entry_landing_time'},
        {'column_name': 'tow_altitude',         'widget_name': 'comboboxentry_tow_altitude'},
        {'column_name': 'counter_start',        'widget_name': 'entry_counter_start'},
        {'column_name': 'counter_landing',      'widget_name': 'entry_counter_landing'},
        {'column_name': 'fk_aircraft',          'widget_name': 'comboboxentry_aircraft_id'},
        {'column_name': 'fk_flight_type',       'widget_name': 'comboboxentry_flight_type'},
        {'column_name': 'fk_pilot',             'widget_name': 'comboboxentry_aircraft_pilot'},
        {'column_name': 'fk_companion',         'widget_name': 'comboboxentry_aircraft_companion'}
    ]

    def __init__(self, db_object):
        self.db_object = db_object
        self.db_table = db_table(self.db_object)

        Portlets.Form.__init__(self, icon_file=RESOURCE_DIR + 'tower_32.png', title='Flugdatenerfassung', glade_file=RESOURCE_DIR + 'forms.glade', window_name='window_flight_record', help_file='user/flight_recording.html')
        self.attributes_lod = self.db_table.attributes
        self.initialize(db_table_object=self.db_table,
                        definition_lod=self.definition,
                        attributes_lod=self.attributes_lod,
                        portlets_lod='')



class ui_table(Portlets.Table):
    definition = \
    [
        {'column_name': 'id',                   'column_number': 0,  'visible': False},
        {'column_name': 'starting_location',    'column_number': 1,  'column_label': 'Startort'},
        {'column_name': 'starting_type',        'column_number': 2,  'column_label': 'Startart', 'visible': False},
        {'column_name': 'starting_date',        'column_number': 3,  'column_label': 'Startdatum'},
        {'column_name': 'starting_time',        'column_number': 4,  'column_label': 'Startzeit'},
        {'column_name': 'landing_location',     'column_number': 5,  'column_label': 'Landeort'},
        {'column_name': 'landing_type',         'column_number': 6,  'column_label': 'Landeart', 'visible': False},
        {'column_name': 'landing_date',         'column_number': 7,  'column_label': 'Landedatum'},
        {'column_name': 'landing_time',         'column_number': 8,  'column_label': 'Landezeit'},
        {'column_name': 'tow_altitude',         'column_number': 9,  'column_label': 'Schlepphöhe',         'visible': False},
        {'column_name': 'counter_start',        'column_number': 10, 'column_label': 'Zählerstand Start',   'visible': False},
        {'column_name': 'counter_landing',      'column_number': 11, 'column_label': 'Zählerstand Landung', 'visible': False},
        {'column_name': 'fk_aircraft',          'column_number': 12, 'column_label': 'Kennzeichen'},
        {'column_name': 'fk_towplane',          'column_number': 13, 'column_label': 'Schleppflugzeug'},
        {'column_name': 'fk_towed_plane_1',     'column_number': 14, 'column_label': 'Geschleppt 1', 'visible': True},
        {'column_name': 'fk_towed_plane_2',     'column_number': 15, 'column_label': 'Geschleppt 2', 'visible': True},
        {'column_name': 'fk_flight_type',       'column_number': 16, 'column_label': 'Flugart'},
        {'column_name': 'fk_pilot',             'column_number': 17, 'column_label': 'Pilot'}
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
        self.Table.set_sort_column('id')


