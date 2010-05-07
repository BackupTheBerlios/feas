#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# This module handles a postgreSQL-database especially for FEAS...

#from widgets import *
from config import *
from functions import *
#from widgets import *

try:
    import pg
except:
    print "unable to initialize PyGreSQL."

# -----------------------------------------------------------------------------
def open_db(dbname=None, host=None, port=None, opt=None, tty=None, user=None, password=None):
    ''' Opens a PostgreSQL database with given parameters,
        returns the connection if the parameters are correct or the error string if not.'''
    
    try:
        if DEBUG: print "Opening SQL connection...",
        DBcnx = pg.connect(dbname, host, port, opt, tty, user, password)
        
        #global pgDB
        #pgDB = pg.DB(dbname, host, port, opt, tty, user, password)
        #print "pgDB:", pgDB
        
        if DEBUG: print "passed."
        return DBcnx
    except Exception, inst:
        if DEBUG: print "FAILED!"
        return inst

def close_db(DBcnx):
    ''' Closes the given database-connection and ensures, that all querys are done.'''
    
    try:
        if DEBUG: print "Closing SQL connection...",
        DBcnx.close()
        if DEBUG: print "passed."
    except Exception, inst:
        if DEBUG: print "FAILED!"
        return inst
    return

def query_sql_command(DBcnx, sql_command):
    ''' Queries a SQL-command and returns the reply of it.'''
    
    if DEBUG: print "Querying SQL-command...",
    try:
        reply = DBcnx.query(sql_command)
        if DEBUG: print sql_command, "\n", "passed."
        return reply
    except Exception, inst:
        if DEBUG: print sql_command; print "FAILED!"; print inst
    return



class db_table:
    def __init__(self, DBcnx, table):
        ''' DBcnx = Database connection
            table = table name as string'''

        self.DBcnx = DBcnx
        self.table = table
        
    # TODO: Put all table-relevant stuff in one class to save vars on functions!
    def get_name(self):
        return self.table

    def get_DBcnx(self):
        return self.DBcnx

    def set_DBcnx(self, DBcnx):
        self.DBcnx = DBcnx

    # Check for non-existing tables and create them if necessary. -----------------
    def verify(self, db_table_layout_list):
        ''' db_table_layout_list = ... '''

        try:
            table_selection = self.DBcnx.query("SELECT * FROM " + self.table)
            if DEBUG: print; print "Table selection of:", self.table; print table_selection
        except Exception, inst:
            if DEBUG: print inst; print "verification error:", inst,
            table_selection = self.create(db_table_layout_list)
        
        verify_result = self.verify_columns(db_table_layout_list)
        return verify_result

    def create(self, db_table_layout_list):
        ''' column_list        = list of columns as [col_name, field_args]
                                 example: ["name", "varchar(40)"]
            dict[db_fieldname] = [db_vartype, gtk.entry_widget_name, gtk.entry_widget_object'''

        sql_command = "CREATE TABLE " + self.table + " ("
        header_length = len(sql_command)

        number_of_columns = len(db_table_layout_list)
        maxlength_field = 0

        for column_dict in db_table_layout_list:
            if len(column_dict['db_field_name']) > maxlength_field:
                maxlength_field = len(column_dict['db_field_name'])

        column_number = 0
        for column_dict in db_table_layout_list:
            if column_number < number_of_columns - 1:
                separator = ", \n"
            else:
                separator = ""

            if column_number == 0:
                header_space = ""
            else:
                header_space = space(header_length)

            command_length = len(column_dict['db_field_name'])
            db_field_name = db_table_layout_list[column_number]['db_field_name']

            if column_dict.has_key('db_field_type'):
                db_field_type = db_table_layout_list[column_number]['db_field_type']
            if column_dict.has_key('db_foreign_table'):
                db_field_type = 'bigint'

            sql_command += header_space + \
                           db_field_name + \
                           space(maxlength_field - command_length + 3) + \
                           db_field_type + separator

            column_number += 1
        sql_command += ")"

        if DEBUG: print sql_command
        if DEBUG: print "creating table " + self.table + "...",
        query_sql_command(self.DBcnx, sql_command)
        table_selection = query_sql_command(self.DBcnx, "SELECT * FROM " + self.table)
        return table_selection

    # Check for non-existing columns and create them if nesseccary. ---------------
    def verify_columns(self, db_table_layout_list):
        ''' Verify the whole database-table-structure basing on db_table_layout_list. '''

        table_selection = ""
        for column_dict in db_table_layout_list:

            if DEBUG: print column_dict['db_field_name'] + "...",
            try:
                column = self.DBcnx.query("SELECT " + column_dict['db_field_name'] + " FROM " + self.table)
                if DEBUG: print "passed."
            except:
                if DEBUG: print "FAILED!"
                if column_dict.has_key('db_field_type'):
                    self.create_column(column_dict['db_field_name'], column_dict['db_field_type'])
                if column_dict.has_key('db_foreign_table'):
                    self.create_column(column_dict['db_field_name'], 'bigint')

            table_selection = query_sql_command(self.DBcnx, "SELECT * FROM " + self.table)
            column_result = table_selection.dictresult()
        return column_result

    def create_column(self, column_name, column_args):
        ''' Creates a new column with given name and given arguments.
                column_name = column header name as string
                column_args = field args as string, for example: "varchar(40)".'''

        if DEBUG: print "    Trying to add column " + column_name + "..."
        sql_command = "ALTER TABLE " + self.table + " ADD COLUMN " + column_name + " " + column_args
        if DEBUG: print "    " + sql_command + "...",
        query_sql_command(self.DBcnx, sql_command)
        return

    def get_column(self, column):
        ''' Returns a list of all entrys which where found in this table with the given column_name. '''
        
        column_selection = query_sql_command(self.DBcnx, "SELECT " + column + " FROM " + self.table)
        try:
            column_entry_list = column_selection.getresult()
            column_entry_list.sort()
            number_of_entrys = len(column_entry_list)
            entry_list = []

            for item in xrange(number_of_entrys):
                entry_list.append(column_entry_list[item][0])
        except:
            return
        return entry_list

    def get_column_with_pk(self, column):
        ''' Returns a list of all entrys which where found in this table with the given column_name. '''
        
        column_selection = query_sql_command(self.DBcnx, "SELECT pk_key_number FROM " + self.table)
        
        try:
            pk_key_number_list = column_selection.getresult()
            pk_key_number_list.sort()
            
            entry_list = []
            for pk_key_number in pk_key_number_list:
                column_entry = self.search_column("pk_key_number", pk_key_number[0], column)[0]
                entry_list.append([pk_key_number[0], column_entry])
        except:
            return
        return entry_list                   
     

    def get_first_key_number(self):
        column_selection = query_sql_command(self.DBcnx, "SELECT pk_key_number FROM " + self.table)
        
        if column_selection <> None:
            column_entry_list = column_selection.getresult()
            column_entry_list.sort()
        else:
            column_entry_list = []

        number_of_entrys = len(column_entry_list)
        first_key_number = 1

        for item in xrange(number_of_entrys):
            if first_key_number == column_entry_list[item][0]:
                first_key_number += 1
            else:
                return first_key_number
        return first_key_number

    def key_number_exists(self, key_number):
        '''
        Returns True if primary key exists and False if not.
        '''

        column_selection = query_sql_command(self.DBcnx, "SELECT pk_key_number FROM " + self.table)
        column_entry_list = column_selection.getresult()
        number_of_entrys = len(column_entry_list)

        for item in xrange(number_of_entrys):
            if column_entry_list[item][0] == key_number:
                return True
        return False

    def select(self):
        column_selection = query_sql_command(self.DBcnx, "SELECT * FROM " + self.table)

        # Prevent error if column_selection returns no results.
        if column_selection <> None:
            dict_length = len(column_selection.dictresult())
        else:
            dict_length = 0

        if dict_length > 0:
            column_dict = column_selection.dictresult()
        else:
            if DEBUG: print "Select returned no matches."
            return 
        return column_dict        

    def get_foreign_cell_text(self, primary_key, foreign_key_column, foreign_table, foreign_column):
        '''
        Returns a single cell, which is located in a foreign table:
            primary_key = pk of column in foreign table which points to the row
            foreign_key_column = fk column name in own table which holds the fk
            foreign_table = db_table object which holds the foreign data
            foreign_column = column_name of the cell-containing column in foreign_table
        '''

        pk_foreign_table = self.search_column("pk_key_number", primary_key, foreign_key_column)[0]
        if pk_foreign_table <> "":
            foreign_cell_content = foreign_table.search_column('pk_key_number', pk_foreign_table, foreign_column)[0]
            if foreign_cell_content <> ():
                return unicode(str(foreign_cell_content), 'latin-1')
        return ''

    def search_column(self, search_column, search_value, target_column):
        '''
        Returns a list of matches after searching a table where:
            search_column = column name of column which is to search
            search_value = value to search for in search_column
            target_column = column name of column which has to return it's value in matching row
        '''
        if type(search_value) == str:
            column_selection = query_sql_command(self.DBcnx, "SELECT * FROM " + self.table + " WHERE " + search_column + " = " + "'" + str(search_value) + "'")
        else:
            column_selection = query_sql_command(self.DBcnx, "SELECT * FROM " + self.table + " WHERE " + search_column + " = " + str(search_value))
        
        # Prevent error if column_selection returns no results.
        if column_selection <> None:
            dict_length = len(column_selection.dictresult())
        else:
            dict_length = 0

        if dict_length > 0:
            column_dict = column_selection.dictresult()
        else:
            if DEBUG: print "Search returned no matches."
            return [()]

        # If there is at least one result, build match_list that contains the target_column entrys of matching search_columns.
        if target_column in column_dict[0]:
            match_list = []
            for match_number in xrange(dict_length):
                if column_dict[match_number][target_column] <> None:
                    match_list.append(column_dict[match_number][target_column])
                else:
                    match_list.append('')
            return match_list
        else:
            if DEBUG: print "target column does not exist in table " + self.table + "."
        return [()]

    def filter(self, filter_function):
        row_selection = query_sql_command(self.DBcnx, "SELECT * FROM " + self.table + " WHERE " + filter_function)
        
        # prevent error if no results are found.
        if row_selection <> None:
            filter_result = row_selection.dictresult()
            return filter_result
        else:
            if DEBUG: print "Filter result contains no matching rows."
        return [()]

    def convert_to_html(self, db_table_layout_list):
        # Lookup if the db is in sync with the needs of out db_fields_layout and fix it if not.
        table_dictlist = self.verify(db_table_layout_list)

        number_of_rows = len(table_dictlist)
        number_of_columns = len(db_table_layout_list)

        if number_of_rows == 0:
            return ""

        # First off, the columns has to be sorted in given order.
        db_table_layout_list.sort(compare_by ('print_table_column'))

        HTMLtable_content = """\
        <h2>Tabelle """ + self.table + """</h2>

        <table>
            <thead>
                <tr>
"""
        for column_number in xrange(number_of_columns):
            hide_column = False
            if db_table_layout_list[column_number].has_key('print_table_column'):
                if db_table_layout_list[column_number]['print_table_column'] == None:
                    hide_column = True

            if hide_column == False:
                if db_table_layout_list[column_number].has_key('column_title'):
                    column_title = str(db_table_layout_list[column_number]['column_title'])
                else:
                    column_title = str(db_table_layout_list[column_number]['db_field_name'])
                
                HTMLtable_content += """\
                    <th>""" + column_title + "</th>" + "\n"

        # Remove last "\n" for better string-form
        HTMLtable_content = HTMLtable_content[0:len(HTMLtable_content)-1]
        HTMLtable_content += "\n" + """\
                </tr>
            </thead>
"""
        HTMLtable_content += """\
            <tbody>
"""
        # This finds the right positions for the content.
        odd_offset = True
        for row_number in xrange(number_of_rows):
            if odd_offset:
                HTMLtable_content += """\
                <tr class="zebrastreifen_ungerade">"""
            else:
                HTMLtable_content += """\
                <tr class="zebrastreifen_gerade">"""
            odd_offset = not odd_offset

            for column_number in xrange(number_of_columns):
                hide_column = False
                if db_table_layout_list[column_number].has_key('print_table_column'):
                    if db_table_layout_list[column_number]['print_table_column'] == None:
                        hide_column = True

                if hide_column == False:
                    column_content = table_dictlist[row_number][db_table_layout_list[column_number]['db_field_name']]
                    if column_content == None:
                        column_content = "-"
                    HTMLtable_content += """
                    <td>""" + str(column_content) + "</td>"
            HTMLtable_content += """
                </tr>
"""
        # Remove last "\n" for better string-form
        HTMLtable_content = HTMLtable_content[0:len(HTMLtable_content)-1]
        HTMLtable_content += """
            </tbody>
        </table>
"""
        return HTMLtable_content

    #def get_field_attributes(self):
    #    return pgDB.get_attnames(self.table)

    def insert_data(self, db_table_layout_list=None, content_dict=None):
        column_selection = query_sql_command(self.DBcnx, "SELECT * FROM " + self.table)
        column_names_list = column_selection.listfields()
        number_of_columns = len(column_names_list)
        if content_dict == None:
            content_dict = get_form_content_dict(db_table_layout_list)

        sql_header = "INSERT INTO " + self.table + " ("
        sql_values = "VALUES ("
        sql_fields = ""

        for item in xrange(number_of_columns):
            if column_names_list[item] in content_dict:
                if str(content_dict[column_names_list[item]]) <> "":
                    sql_fields += column_names_list[item]
                    if type(content_dict[column_names_list[item]]) == str and content_dict[column_names_list[item]] <> "NULL":
                        container = "\'"
                    else:
                        container = ""
                    sql_values += container + str(content_dict[column_names_list[item]]).encode("latin-1") + container
                    sql_fields += ", "
                    sql_values += ", "
            else:
                if DEBUG: print "...", str(column_names_list[item]), "not in dictionary!"

        sql_fields = sql_fields[0:len(sql_fields)-2] + ")" + "\n"
        sql_values = sql_values[0:len(sql_values)-2] + ")" + "\n"
        sql_command = sql_header + sql_fields + sql_values

        if DEBUG: print sql_command
        if DEBUG: print "Inserting dataset...",
        query_sql_command(self.DBcnx, sql_command)
        return

    def update_data(self, key_number, db_table_layout_list=None, content_dict=None):
        column_selection = query_sql_command(self.DBcnx, "SELECT * FROM " + self.table)
        column_names_list = column_selection.listfields()
        number_of_columns = len(column_names_list)
        if content_dict == None:
            content_dict = get_form_content_dict(db_table_layout_list)

        sql_command = "UPDATE " + self.table + " SET" + "\n"

        for item in xrange(number_of_columns):
            if column_names_list[item] in content_dict:
                if str(content_dict[column_names_list[item]]) <> "":
                    sql_command += "    " + column_names_list[item] + " = "
                    if type(content_dict[column_names_list[item]]) == str and content_dict[column_names_list[item]] <> "NULL":
                        container = "\'"
                    else:
                        container = ""
                    sql_command += container + str(content_dict[column_names_list[item]]).encode("latin-1") + container + ",\n"
            else:
                if DEBUG: print "...", str(column_names_list[item]), "not in dictionary!"

        sql_command = sql_command[0:len(sql_command)-2] + "\n"

        sql_command += "WHERE" + "\n"
        sql_command += "    pk_key_number = " + str(key_number)

        if DEBUG: print; print sql_command; print
        if DEBUG: print "Updating dataset...",
        query_sql_command(self.DBcnx, sql_command)

    def delete_data(self, key_number=None, where=None):
        if where == None:
            sql_command  = "DELETE FROM " + self.table + " WHERE pk_key_number = " + str(key_number) +"\n"
        else:
            sql_command  = "DELETE FROM " + self.table + " WHERE " + where +"\n"

        if DEBUG: print sql_command
        if DEBUG: print "Inserting dataset...",
        query_sql_command(self.DBcnx, sql_command)
        return

#TODO: On multiuser, there has to be a thread which checks for changes to keep the treeview up to date!

# Widget functions ------------------------------------------------------------
def get_widget_from_db_table_layout(db_table_layout_list, widget_name):
    number_of_entrys = len(db_table_layout_list)
    for entry_number in xrange(number_of_entrys):
        if widget_name == db_table_layout_list[entry_number]['gtk_widget_name']:
            widget = db_table_layout_list[entry_number]['gtk_widget_object']
            return widget
    return

def get_form_content_dict(db_table_layout_list):
    ''' Gets the whole content of a form, defined by a dictionary.
        Inputs: fields_dict[field_name] = widget_object, data_type
        Returns: content_dict[field_name] = widget_content'''

   # fields_list = fields_dict.keys()
    number_of_fields = len(db_table_layout_list)

    content_dict = {}
    for column_number in xrange(number_of_fields):
        # This is needed if no gtk_widget_object is given in dict!
        if db_table_layout_list[column_number].has_key('gtk_widget_object'):
            widget = db_table_layout_list[column_number]['gtk_widget_object']
        else:
            widget = None

        if db_table_layout_list[column_number].has_key('db_field_type'):
            if db_table_layout_list[column_number]['db_field_type'].startswith("varchar"):
                data_type = str
            if db_table_layout_list[column_number]['db_field_type'].startswith("money"):
                data_type = str
            if db_table_layout_list[column_number]['db_field_type'].startswith("date"):
                data_type = str
            if db_table_layout_list[column_number]['db_field_type'].startswith("time"):
                data_type = str
            if db_table_layout_list[column_number]['db_field_type'].startswith("integer"):
                data_type = int
            if db_table_layout_list[column_number]['db_field_type'].startswith("bigint"):
                data_type = int
            if db_table_layout_list[column_number]['db_field_type'].startswith("bool"):
                data_type = bool
        if db_table_layout_list[column_number].has_key('db_foreign_key_column'):
            data_type = int

        if widget <> None:
            if widget.get_name().startswith("entry"):
                # This handles invalid literal errors on int-type-conversion!
                try:
                    # Check, if a datefield is there and convert to Postgres-compatible date
                    content_dict[db_table_layout_list[column_number]['db_field_name']] = data_type(widget.get_text())
                    if db_table_layout_list[column_number]['db_field_type'].startswith("date"):
                        if content_dict[db_table_layout_list[column_number]['db_field_name']] <> "":
                            content_dict[db_table_layout_list[column_number]['db_field_name']] = convert_gmdate_to_usdate(content_dict[db_table_layout_list[column_number]['db_field_name']])
                except Exception, inst:
                    if DEBUG: print inst
                    content_dict[db_table_layout_list[column_number]['db_field_name']] = data_type(0)
            if widget.get_name().startswith("comboboxentry"):
                if db_table_layout_list[column_number].has_key('db_foreign_table'):
                    combobox_content = get_comboboxentry_selection(widget)[0]
                    #print "...",widget.get_name(), "...", combobox_content
                    if combobox_content <> ():
                        content_dict[db_table_layout_list[column_number]['db_field_name']] = data_type(combobox_content)
                    if widget.child.get_text() == "":
                        content_dict[db_table_layout_list[column_number]['db_field_name']] = "NULL"
                else:
                    content_dict[db_table_layout_list[column_number]['db_field_name']] = data_type(widget.child.get_text())
            if widget.get_name().startswith("check"):
                content_dict[db_table_layout_list[column_number]['db_field_name']] = data_type(widget.get_active())
            if widget.get_name().startswith("textview"):
                text_buffer = widget.get_buffer()
                start_iter = text_buffer.get_start_iter()
                end_iter = text_buffer.get_end_iter()
                content_dict[db_table_layout_list[column_number]['db_field_name']] = data_type(text_buffer.get_text(start_iter, end_iter))
    return content_dict


# Experimental needs ----------------------------------------------------------
def create_role(DBcnx, role, password):
    sql_command = """\
CREATE ROLE """ + role + """ LOGIN
    PASSWORD '""" + password + """'
    SUPERUSER INHERIT CREATEDB CREATEROLE;"""

    query_sql_command(DBcnx, sql_command)
    return





