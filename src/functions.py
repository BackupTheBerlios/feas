#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# -----------------------------------------------------------------------------
# Standard-Funktionen
# (c) by Mark Muzenhardt
# -----------------------------------------------------------------------------

import os.path
import webbrowser
import time
import datetime
import ConfigParser

#from widgets import dialog

# Time and date functions ------------------------------------------------------
def get_usdate_str():
    year = str(time.gmtime()[0])
    month = str(time.gmtime()[1])
    day = str(time.gmtime()[2])

    if len(month) == 1: month = "0" + month
    if len(day) == 1: day = "0" + day

    usdate_str = year + "-" + month + "-" + day
    return usdate_str

def get_gmtime_str():
    hour = str(time.gmtime()[3])
    minute = str(time.gmtime()[4])
    second = str(time.gmtime()[5])

    if len(hour) == 1: hour = "0" + hour
    if len(minute) == 1: minute = "0" + minute
    if len(second) == 1: second = "0" + second

    gmtime_str = hour + ":" + minute + ":" + second
    return gmtime_str

def get_gmdate_str():
    year = str(time.gmtime()[0])
    month = str(time.gmtime()[1])
    day = str(time.gmtime()[2])

    if len(month) == 1: month = "0" + month
    if len(day) == 1: day = "0" + day

    gmdate_str = day + "." + month + "." + year
    return gmdate_str

def get_gmdate_ymd():
    year = time.gmtime()[0]
    month = time.gmtime()[1]
    day = time.gmtime()[2]
    return year, month, day

def convert_gmdate_to_usdate(gmdate_str):
    try:
        year = str(gmdate_str[6:10])
        month = str(gmdate_str[3:5])
        day = str(gmdate_str[0:2])

        usdate_str = year + "-" + month + "-" + day
        return usdate_str
    except Exception, inst:
        print inst
        return None

def convert_usdate_to_gmdate(usdate_str):
    try:
        year = usdate_str[0:4]
        month = usdate_str[5:7]
        day = usdate_str[8:10]

        gmdate_str = day + "." + month + "." + year
        return gmdate_str
    except Exception, inst:
        print inst
        return None

def validate_datestring(datestring):
    try:
        day = int(datestring[0:2])
        month = int(datestring[3:5])
        year = int(datestring[6:10])
        if day <= 31 and day >= 0 and \
           month <= 12 and month >= 0 and \
           year <= 2999 and year >= 0:
            validity = True
        else:
            validity = False
    except ValueError:
        validity = False

    if len(datestring) <> 10:
        validity = False
    if datestring == "":
        validity = True
    return validity

def validate_timestring(timestring):
    try:
        hour, minute, second = split_timestring(timestring)

        if hour <= 23 and hour >= 0 and \
           minute <= 59 and minute >=0 and \
           second <= 59 and second >=0:
            validity = True
        else:
            validity = False
    except ValueError:
        validity = False

    if len(timestring) < 5:
        validity = False
    return validity

def split_timestring(timestring):
    hour = int(timestring[0:2])
    minute = int(timestring[3:5])
    if len(timestring) > 5:
        second = int(timestring[6:8])
    else:
        second = 0
    return hour, minute, second

def split_gmdatestring(datestring):
    day = int(datestring[0:2])
    month = int(datestring[3:5])
    year = int(datestring[6:10])
    return day, month, year

def get_gmdatetime_deltastring(start_date="", start_time="", end_date="", end_time=""):
    if start_date <> "":
        start_day, start_month, start_year = split_gmdatestring(start_date)
    if start_time <> "":
        start_hour, start_minute, start_second = split_timestring(start_time)
    if end_date <> "":
        end_day, end_month, end_year = split_gmdatestring(end_date)
    if end_time <> "":
        end_hour, end_minute, end_second = split_timestring(end_time)

    try:
        start_datetime = datetime.datetime(start_year, start_month, start_day, start_hour, start_minute, start_second)
        end_datetime = datetime.datetime(end_year, end_month, end_day, end_hour, end_minute, end_second)
        datetime_delta_string = str(end_datetime - start_datetime)
        return datetime_delta_string
    except:
        return ""

# Inifile-Functions -----------------------------------------------------------
def load_ini_file(filename):
    config_parser = ConfigParser.ConfigParser()

    list_of_filenames = config_parser.read(filename)
    return config_parser

def parse_ini_file(config_parser, section, option):
    try:
        value = config_parser.get(section, option)
    except Exception, inst:
        print inst
        value = None
    return value

def save_ini_file(filename, ini_text):
    ini_file = open(filename, "w")
    ini_file.write(ini_text)
    ini_file.close()
    return

# Browser- and Text- Functions ------------------------------------------------
def startbrowser(FileName, parent=None):
    '''OS independent way to open local html-files in the default webbrowser
       Version 1.0 by Mark Muzenhardt'''

    AbsPath = os.path.abspath(FileName)
    Url = "file://" + AbsPath

    try:
        webbrowser.open(Url, new=0, autoraise=1)
    except Exception, inst:
        dialog ("Fehler!", parent, str(inst), "error")

def space(items, charakter=" "):
    '''this simple spits out space charakters as much as given
       Version 1.0 by Mark Muzenhardt'''

    string = ""
    for char in xrange(items):
        string = string + charakter
    return string


class time_string:
    def check(self, time_string):
        return True

    def convert(self, time_string, from_format, to_format):
        time_string = None
        return time_string


class date_string:
    def check(self, date_string):
        return True

    def convert(self, date_string, from_format, to_format):
        date_string = None
        return date_string

# This is needed to compare dictlists with sort(compare_by ('key'))
def compare_by (fieldname):
   def compare_two_dicts (a, b):
      if a.has_key(fieldname) and b.has_key(fieldname):
          return cmp(a[fieldname], b[fieldname])
      return 0
   return compare_two_dicts

# HTML-functions temporarily --------------------------------------------------
def HTMLheader(title="", body=""):
    # TODO: Replace with JINJA2, cause ninja rockz!
    text = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
                      "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <title>""" + title + """</title>
        <link rel="stylesheet" href="css/common.css">
        <link rel="stylesheet" media="screen" href="css/screen.css">
        <link rel="stylesheet" media="print" href="css/print.css">
    </head>

    <body>
""" + body + """\
    </body>
</html>
"""
    return text
