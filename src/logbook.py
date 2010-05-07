# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS logbook V0.8 alpha
# (c) by Mark Muzenhardt
#===============================================================================

from dbGUIapi.DBapi import SQLdb


class main:
    pass



class db_table(SQLdb.table):
    attributes =  \
    [
        {'column_name': 'id'       , 'data_type': 'bigint'  , 'is_nullable': False, 'is_primary_key': True},
        {'column_name': 'timestamp', 'data_type': 'datetime'},
        {'column_name': 'text'     , 'data_type': 'varchar' , 'character_maximum_length': 255},
        {'column_name': 'categorys', 'data_type': 'varchar' , 'character_maximum_length': 255}
    ]

    def __init__(self, db_object):
        SQLdb.table.__init__(self, db_object, 'logbook')
        differences_lod = self.check_attributes(self.attributes, action='analyze')
        print 'logbook diff:', differences_lod