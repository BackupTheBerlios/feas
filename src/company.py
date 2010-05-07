# -*- coding: iso-8859-1 -*-

#===============================================================================
# exSpedition company module
# (c) by Mark Muzenhardt
#===============================================================================


class company:
    def __init__(self, db_object, id):
        self.db_table = db_table(db_object)


    def dummy(self):
        pass



class db_table(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id'               , 'data_type': 'bigint' , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'name'             , 'data_type': 'varchar', 'character_maximum_length': 40},
        {'column_name': 'created',           'data_type': 'datetime'},
        {'column_name': 'updated',           'data_type': 'datetime'},
        {'column_name': 'deactivated'      , 'data_type': 'bool'}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'members')
        differences_lod = self.check_attributes(self.attributes, action='analyze')
        print differences_lod



class form:
    attributes = \
    [
        {'column_name': 'id'            , 'widget_name': 'entry_key_number'},
        {'column_name': 'title'         , 'widget_name': 'comboboxentry_title'},
        {'column_name': 'firstname'     , 'widget_name': 'entry_firstname'},
        {'column_name': 'lastname'      , 'widget_name': 'entry_lastname'},
        {'column_name': 'company'       , 'widget_name': 'entry_company'},
        {'column_name': 'show_as'       , 'widget_name': 'entry_show_as'},
        {'column_name': 'birthday'      , 'widget_name': 'entry_birthday'},
        {'column_name': 'post_code'     , 'widget_name': 'entry_post_code'},
        {'column_name': 'city'          , 'widget_name': 'entry_city'},
        {'column_name': 'street'        , 'widget_name': 'entry_street'},
        {'column_name': 'phone_personal', 'widget_name': 'entry_phone_personal'},
        {'column_name': 'phone_business', 'widget_name': 'entry_phone_business'},
        {'column_name': 'phone_mobile'  , 'widget_name': 'entry_phone_mobile'},
        {'column_name': 'email_personal', 'widget_name': 'entry_email_personal'},
        {'column_name': 'email_business', 'widget_name': 'entry_email_business'}
    ]



class treeview:
    attributes = \
    [
        {'column_name': 'id'            , 'column_number':  0, 'visible': False},
        {'column_name': 'title'         , 'column_number':  1, 'column_label': 'Anrede'},
        {'column_name': 'firstname'     , 'column_number':  5, 'column_label': 'Vorname', 'gtk_column_hide': True},
        {'column_name': 'lastname'      , 'column_number':  6, 'column_label': 'Nachname', 'gtk_column_hide': True},
        {'column_name': 'company'       , 'column_number':  3, 'column_label': 'Firma'},
        {'column_name': 'show_as'       , 'column_number':  2, 'column_label': 'Zeige als'},
        {'column_name': 'birthday'      , 'column_number':  4, 'column_label': 'Geburtsdatum'},
        {'column_name': 'post_code'     , 'column_number':  7, 'column_label': 'Postleitzahl'},
        {'column_name': 'city'          , 'column_number':  8, 'column_label': 'Stadt'},
        {'column_name': 'street'        , 'column_number':  9, 'column_label': 'Straße'},
        {'column_name': 'phone_personal', 'column_number': 10, 'column_label': 'Telefon privat'},
        {'column_name': 'phone_business', 'column_number': 11, 'column_label': 'Telefon gesch.'},
        {'column_name': 'phone_mobile'  , 'column_number': 12, 'column_label': 'Mobiltelefon'},
        {'column_name': 'email_personal', 'column_number': 13, 'column_label': 'eMail privat'},
        {'column_name': 'email_business', 'column_number': 14, 'column_label': 'eMail gesch.'}
    ]

