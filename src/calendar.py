# -*- coding: iso-8859-1 -*-

#===============================================================================
# FEAS calendar module. Introduced in v0.8 alpha.
# by Mark Muzenhardt, published under BSD-License.
#===============================================================================

#from BaseUI import Portlets
#from BaseUI.DB import SQLdb
import gtk
import math

from config import *


class main:
    def __init__(self, db_object=None):
        #self.db_object = db_object
        #self.db_table = db_table(self.db_object)

        self.calendar = calendar()
        #self.form = form(self.db_object)
        #self.table = table(self.db_object, self.form)

        self.portlet = self.calendar #.portlet #self.table.portlet
        self.toolbar = None #self.calendar.toolbar


    def update(self):
        pass



class calendar(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose_event", self.expose)
        
        
    def expose(self, widget, event):
        self.context = widget.window.cairo_create()
        
        # set a clip region for the expose event
        self.context.rectangle(event.area.x, event.area.y,
                               event.area.width, event.area.height)
        self.context.clip()
        self.draw(self.context)
        return False
    
    
    def draw(self, context):
        rect = self.get_allocation()
        x = rect.width / 2
        y = rect.height / 2
        radius = min(rect.width / 2, rect.height / 2)
        
        # clock back
        context.arc(x, y, radius, 0, 2 * math.pi)
        context.set_source_rgb(1, 1, 1)
        context.fill_preserve()
        context.set_source_rgb(0, 0, 0)
        context.stroke()
        
        # clock ticks
        for i in xrange(12):
            context.save()
            
            if i % 3 == 0:
                inset = 0.2 * radius
            else:
                inset = 0.1 * radius
                context.set_line_width(0.5 * context.get_line_width())
            
            context.move_to(x + (radius - inset) * math.cos(i * math.pi / 6),
                            y + (radius - inset) * math.sin(i * math.pi / 6))
            context.line_to(x + radius * math.cos(i * math.pi / 6),
                            y + radius * math.sin(i * math.pi / 6))
            context.stroke()
            context.restore()
            
            
