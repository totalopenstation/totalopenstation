#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: gui/gui.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import gobject
import gtk
import gtk.glade
import pango
import os

from models.models import models
from output.formats import formats

# FIXME this path is relative to the root source directory
GLADEFILE = "gui/tops.glade"


class AboutDialog(object):

    def __init__(self):
        self.gladefile = GLADEFILE
        self.widgetTree1 = gtk.glade.XML(self.gladefile, 'aboutdialog1')
        self.aboutdialog1 = self.widgetTree1.get_widget('aboutdialog1')
        self.aboutdialog1.run()
        self.aboutdialog1.destroy()


class ExportDialog(object):

    def __init__(self):
        self.gladefile = GLADEFILE
        self.widgetTree1 = gtk.glade.XML(self.gladefile, 'export_dialog1')
        self.export_dialog1 = self.widgetTree1.get_widget('export_dialog1')

        # model combo box
        self.modelsListStore = gtk.ListStore(gobject.TYPE_STRING)
        for m, n in models.items():
            self.modelsListStore.append([m])
        self.combobox_input = self.widgetTree1.get_widget('combobox_input')
        self.combobox_input.set_model(model=self.modelsListStore)
        cell = gtk.CellRendererText()
        self.combobox_input.pack_start(cell, True)
        self.combobox_input.add_attribute(cell, 'text', 0)

        # output format combo box
        self.outputFormatsListStore = gtk.ListStore(gobject.TYPE_STRING)
        for m, n in formats.items():
            self.outputFormatsListStore.append([m])
        self.combobox_output = self.widgetTree1.get_widget('combobox_output')
        self.combobox_output.set_model(model=self.outputFormatsListStore)
        cell1 = gtk.CellRendererText()
        self.combobox_output.pack_start(cell, True)
        self.combobox_output.add_attribute(cell, 'text', 0)

        self.export_dialog1.run()
        self.export_dialog1.destroy()


class TotalOpenGUI(object):
    '''Implements the main program window.'''

    def __init__(self):

        self.gladefile = GLADEFILE
        self.widgetTree = gtk.glade.XML(self.gladefile, 'window1')
        self.widgetTree.signal_autoconnect(self)
        self.window1 = self.widgetTree.get_widget('window1')
        self.window1.show_all()

        self.textView = self.widgetTree.get_widget('textview1')
        self.textBuffer = gtk.TextBuffer()
        self.textView.set_buffer(self.textBuffer)
        mono_font_desc = pango.FontDescription("monospace")
        self.textView.modify_font(mono_font_desc)

    def gtk_main_quit(self, widget, event=None):
        gtk.main_quit()

    def on_open_menuitem_activate(self, widget):
        file_open = gtk.FileChooserDialog(title="Select file to open",
                    action=gtk.FILE_CHOOSER_ACTION_OPEN,
                    buttons=(gtk.STOCK_CANCEL,
                             gtk.RESPONSE_CANCEL,
                             gtk.STOCK_OPEN,
                             gtk.RESPONSE_OK))
        if file_open.run() == gtk.RESPONSE_OK:
            result = file_open.get_filename()
        file_open.destroy()
        self.textBuffer.set_text(open(result).read())

    def on_save_menuitem_activate(self, widget):
        file_save = gtk.FileChooserDialog(title="Select destination file",
                    action=gtk.FILE_CHOOSER_ACTION_SAVE,
                    buttons=(gtk.STOCK_CANCEL,
                        gtk.RESPONSE_CANCEL,
                        gtk.STOCK_SAVE,
                        gtk.RESPONSE_OK))
        if file_save.run() == gtk.RESPONSE_OK:
            result = file_save.get_filename()
        file_save.destroy()

        self.iterstart = self.textBuffer.get_start_iter()
        self.iterend = self.textBuffer.get_end_iter()

        # FIXME handle overwriting an existing file (ask the user)
        e = open(result, 'w')
        e.write(self.textBuffer.get_text(self.iterstart, self.iterend))
        e.close()

    def export_dialog(self, widget):
        ex = ExportDialog()
        input_model = ex.combobox_input.get_active()
        output_model = ex.combobox_output.get_active()
        if (output_model < 0) or (input_model < 0):

            md = gtk.MessageDialog(parent=None,
                            type=gtk.MESSAGE_ERROR,
                            buttons=gtk.BUTTONS_CLOSE,
                            message_format="Please choose input and output")
        else:
            self.iterstart = self.textBuffer.get_start_iter()
            self.iterend = self.textBuffer.get_end_iter()
            data = self.textBuffer.get_text(self.iterstart, self.iterend)
            exec('from models.%s import ModelParser' % (
                models[ex.modelsListStore[input_model][0]],
                ))
            exec('from output.%s import TotalOpen%s as Output' % (
                formats[ex.outputFormatsListStore[output_model][0]],
                ex.outputFormatsListStore[output_model][0],
                ))
            parsed_data = ModelParser(data)
            parsed_points = parsed_data.points

            file_save = gtk.FileChooserDialog(title="Select destination file",
                    action=gtk.FILE_CHOOSER_ACTION_SAVE,
                    buttons=(gtk.STOCK_CANCEL,
                             gtk.RESPONSE_CANCEL,
                             gtk.STOCK_SAVE,
                             gtk.RESPONSE_OK))
            if file_save.run() == gtk.RESPONSE_OK:
                result = file_save.get_filename()
            file_save.destroy()

            # FIXME handle overwriting an existing file (ask the user)
            output = Output(parsed_points, result)

    def about_dialog(self, widget):
        AboutDialog()

if __name__ == '__main__':
    print('Please use the totalopenstation-gui2.py module in the root source.')
