#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: totalopenstation-gui.py
# Copyright 2008-2014 Stefano Costa <steko@iosa.it>
# Copyright 2010,2012 Luca Bianconi <luxetluc@yahoo.it>
#
# This file is part of Total Open Station.
#
# Total Open Station is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Total Open Station is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Total Open Station.  If not, see
# <http://www.gnu.org/licenses/>.

import serial
import gettext
import atexit

from time import sleep

from Tkinter import *
from tkMessageBox import showwarning, showinfo, askokcancel
import tkSimpleDialog
import tkFileDialog

import totalopenstation

from totalopenstation.models import BUILTIN_MODELS
from totalopenstation.formats import BUILTIN_INPUT_FORMATS
from totalopenstation.output import BUILTIN_OUTPUT_FORMATS
from totalopenstation.utils.upref import UserPrefs

t = gettext.translation('totalopenstation', './locale', fallback=True)
_ = t.lgettext


def scan():
    """scan for available ports. return a list of tuples (num, name).

    Part of pySerial (http://pyserial.sf.net)  (C)2002-2003 <cliechti@gmx.net>
    """

    # TODO move this function in a separate module together with scanwin32.py
    # and add conditional loading depending on the operating system

    available = []
    for i in range(256):
        try:
            s = serial.Serial(i)
            available.append((i, s.portstr))
            s.close()   #explicit close 'cause of delayed GC in java
        except serial.SerialException:
            pass
    return available

# logo GIF image encoded as base64 string
# this way we don't need external an external image file
logo_data = '''
R0lGODlhMAAwAOfIAC40NjA2NzY6ODw+O0g8MEBBP09JOVRMO1hPP0NDQk9MQVRWVFhaV1tcW2Rn\n
ZGZpZm1ubHFzbnV3c3h7dnx+ebw/P8wAAM8NDdEGBtQLC9gNDcUcHM4ZGdMTE98XF9MdHd8ZGc8q\n
KtM3N9Y7O+8pKeM7O/A0NJ1QEbV6MM5cAMFeDdBfBcJfEcVgDc1lDtFgA9xqA9BjCtVoCcNhE8hm\n
FMVlGtRvHdVyFdJzHeVuAexzAPJ2APV5AfV+CsduJspzLtJ0IMx3M8t4Nd5aWuRJSPFERPFLS+Nc\n
XNZ7W990dOJjY+hnZ+Jsa/FgYPFsbON0dPV2dvR5eX6AfL2JPPaDDPaFE/eKFPaGGfeNG/iSHd6B\n
Jd6DKd2FMtyEPMmRPOmNKPeMJO+XLfeSJPiWIfmZJfWULPmbKumQMOmVPveVNfKcM/mfMfmfOvqg\n
LfqkMvmlO/yuPYCCfc+ESNCFSMmZT9WSXPGgRPerQvuuQvGiSPerSvquSfywQ/yySfemVfinV/ev\n
U/qsUfuzVPy4VPq1WPy6Xdqhc9yoffmvYvmxZfy+Zfq1avu8beereuiufvu7c/3CbPzDdPzEe/3J\n
fYOFgYeIg4qNh46RjJCUkLGOjqmsprW1tb66ut+ehe2Hh+2Li/aWlveYmN+wi+Cvh+CwieK3leW9\n
nPrHgP3Lgv3Oif3Skv3WnenHrenIrv7apvXTrf7fsfLTuv7gtv7iuMHBwcrKytra2u7Vwunazeve\n
0/Lf0O3h1+3h2PPg0v7t1Pbp3+Xl5ezs7PHl5fHr6/vs7Pnx6vPz8/z38///////////////////\n
////////////////////////////////////////////////////////////////////////////\n
////////////////////////////////////////////////////////////////////////////\n
/////////////////////////////////////////////////////yH5BAEAAP8ALAAAAAAwADAA\n
AAj+AP8JHEiwoMBYNlIoXJjCRiyDECNKhGjjla+LFx/98WNjoseP/xotlKWqZEkeORim6AKy5cAU\n
s1ylUKWoZk0eM1OhiqQohUuXMOGkiASnaFGcqo6m8fkTZNATCgIEMDAFDs5UR8swbeoRppcEEyhR\n
cDDAC05UR8Fs5SoRJgJKDBIssIQJAc5JadeyhQhTQKUEmxpUuiTg7tErevcWhHlgwgIGEKQ8OICT\n
qNUqiRW/nOWlgARKjgfQ0QrpaI/Mmv8FRUFAKoETC0tbxZma76yjtF8qwo1ac9DZKl8U4l3b4G81\n
YZIrV2OUR+7iA1fImgXL1SpVqSZFglRoUB8+zl/+QCfoSKV5lY7GRwTAII4mTZciLACgfuIRAPjz\n
51dSH+ITT05gYMGAA2LQxBFP9EcQMR+AUgIUEDZhhAkklBBFB8QoKNATn4SiARQkhCiiBlEskaCC\n
DIJihAUgihiiBUVcmGF/TxARCgksuvgiCVGUcGJ9TxCYo45CMqEgKVwwwgOLRhDJAyNckNJfMSxE\n
gsWSFgxB4AUD8oBFJCwUU18daATCgw4zpIAIFWxakcIMOvAQCBp1qNcLDZFQwYMLpqSQCJtUYJGC\n
KS7wQAUjNPQynhB5sIGSD6otYsWkgv7jQw48sGGHENC1AoQizrVwS6STWiGGT7e04FwhOLRSXA3+\n
gIjBAwxzCJTCIljkeqpAc8DAgxh61FDbKFsIwsMOKvxiKyNZNGsGU7+osAMPe2gximbFzEBIFTzI\n
YMhLj4wh7rMDGSIDD1XsMYOYe9VxxhtnzkBQCo+QYe8aa8HJwxpf1MmWLjQIoief80ZixsFurEUo\n
Dz3gQYMubAWhhhmPLiZJGxi/odelPIxRRhBcsYJDH6GOOq8kbqSscUGpOufGDaw0VcMbV8Igh3Eo\n
pyyUQXL4aoUZwrpUyg1uxMvLQMEkncIpbzSNRwpJBzPQLvqacYMoLnVCoBC5/BN10sCkgFZRfKQA\n
zNdS4/IDgUi49AEIHSQh0NfA1C22UX2YXfdx1wKNkIEHFrQUjAUZiDDM3FHXHfYpqHB3h95nRy2Q\n
MB0IKLVHwNBiQQWc2IJ04sAcEsNCMRyyt+QC2cLJBhbQAsxHwdhiy+sEoZ20BTjafvlAwMi+e23B\n
ABNCBhycraFEwdSSiQWZ1PL78Qb1TrtiAQEAOw==\n'''

class StatusBar(Frame):
    '''A status bar for Tkinter applications.

    From: http://effbot.org/tkinterbook/tkinter-application-windows.htm
    '''

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class AboutDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        title = "Total Open Station %s" % totalopenstation.__version__
        message = _("""
Total Open Station is copyright 2008-2015 Luca Bianconi, Stefano Costa
and the IOSA project, under the GNU GPL v3 or any later version.

http://tops.iosa.it/

The application logo is copyright 2008 Lapo Calamandrei under the same
license.""")

        self.logo_data = logo_data
        self.logo = PhotoImage(data=self.logo_data)
        Label(master, image=self.logo).pack()

        Label(master, text=title, font=("Helvetica", "16", "bold")).pack()
        Label(master, text=message).pack()

    def buttonbox(self):
        box = Frame(self)
        w = Button(box,
                   text="OK",
                   width=10,
                   command=self.cancel,
                   default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("&lt;Return>", self.cancel)
        self.bind("&lt;Escape>", self.cancel)
        box.pack()


class DownloadDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        title = "Total Open Station download"
        message = _("""
Press OK when you're ready to download.\n
Depending on your device, you may need to start the transfer from\n
the total station menu.""")

        Label(master, text=title, font=("Helvetica", "16", "bold")).pack()
        self.msg_var = StringVar()
        self.msg_var.set(message)
        self.msg = Label(master, textvariable=self.msg_var)
        self.msg.pack()

    def apply(self):
        self.result = True


class ConnectDialog(tkSimpleDialog.Dialog):

    def __init__(self, parent, cs):
        self.conn_str = cs
        tkSimpleDialog.Dialog.__init__(self, parent)

    def body(self, master):
        title = _("waiting for data from device")
        message1 = _("Connection initialized with the following parameters:\n")
        params = "%s\n" % self.conn_str
        message2 = _("\nStart the download procedure on the device.\n")
        message2 = message2 + _("Press OK when done.")
        Label(master, bitmap="hourglass").pack()
        Label(master, text=title, font=("Helvetica", "16", "bold")).pack()
        Label(master, text=message1).pack()
        t = Text(master,
             width=80)
        t.insert(END, params)
        t.pack()
        Label(master, text=message2, fg="red").pack()


class ProcessDialog(tkSimpleDialog.Dialog):

    def __init__(self, parent, data):
        self.data = data
        self.format = ''
        tkSimpleDialog.Dialog.__init__(self, parent)

    def body(self, master):
        title = _("Choose output format and destination file")
        question = _("Output format:\n")
        top_frame = Frame(master)
        top_frame.pack(side=TOP, padx=5, pady=5)

        control_panel0 = Frame(master)
        control_panel0.pack(
            side=TOP,
            expand=YES,
            anchor=S,
            fill=Y, padx=5, pady=5)
        bottom_frame = Frame(master)
        bottom_frame.pack(side=TOP, anchor=S)

        Label(top_frame, bitmap="question").pack(side=TOP, anchor=N)
        Label(top_frame, text=title).pack(side=TOP, anchor=N)
        output_frame = Frame(control_panel0, relief=RIDGE, bd=1)
        input_frame = Frame(control_panel0, relief=RIDGE, bd=1)
        input_frame.pack(side=TOP)
        output_frame.pack(side=TOP)

        params = "%s\n" % self.data

        Label(input_frame, text=_('Input format'), width=20).pack(side=LEFT)

        self.input_format = StringVar()
        self.input_format.set(self.format)
        input_format_entry = Menubutton(input_frame,
                                        text=_("choose a format"),
                                        textvariable=self.input_format,
                                        relief=RAISED,
                                        width=24)
        input_format_entry.menu = Menu(input_format_entry, tearoff=0)
        input_format_entry["menu"] = input_format_entry.menu

        for k, v in sorted(BUILTIN_INPUT_FORMATS.items()):
            input_format_entry.menu.add_radiobutton(
                label=v[2],
                variable=self.input_format,
                value=k)
        input_format_entry.pack(side=LEFT, anchor=W)

        Label(output_frame, text=_('Output format'), width=20).pack(side=LEFT)

        self.output_format = StringVar()
        self.output_format.set(self.format)
        output_format_entry = Menubutton(output_frame,
                                        text=_("choose a format"),
                                        textvariable=self.output_format,
                                        relief=RAISED,
                                        width=24)
        output_format_entry.menu = Menu(output_format_entry, tearoff=0)
        output_format_entry["menu"] = output_format_entry.menu

        for k, v in sorted(BUILTIN_OUTPUT_FORMATS.items()):
            output_format_entry.menu.add_radiobutton(
                label=v[2],
                variable=self.output_format,
                value=k)
        output_format_entry.pack(side=LEFT, anchor=W)

    def validate(self):
        # do nothing if input is empty
        if self.output_format.get() == '' or self.input_format.get() == '':
            return False
        else:
            return True

    def apply(self):
        '''Export data in the required output format'''

        inputclass = BUILTIN_INPUT_FORMATS[self.input_format.get()]

        # import input format parser
        if isinstance(inputclass, tuple):
            try:
                # builtin format parser
                mod, cls, name = inputclass
                inputclass = getattr(
                    __import__('totalopenstation.formats.' + mod, None, None, [cls]), cls)
            except ImportError, msg:
                showwarning(_('Import error'),
                            _('Error loading the required input module: %s' % msg))

        # import output format writer
        of_lower = str(self.output_format.get()).lower()
        outputclass = BUILTIN_OUTPUT_FORMATS[self.output_format.get()]
        if isinstance(outputclass, tuple):
            try:
                # builtin output builder
                mod, cls, name = outputclass
                outputclass = getattr(
                    __import__('totalopenstation.output.' + mod, None, None, [cls]), cls)
            except ImportError, msg:
                showwarning(_('Import error'),
                            _('Error loading the required output module: %s' % msg))

        # no point in parsing before the output format has been imported
        parsed_data = inputclass(self.data)
        parsed_points = parsed_data.points
        output = outputclass(parsed_points)
        sd = tkFileDialog.asksaveasfilename(defaultextension='.%s' % of_lower)

        try:
            sd_file = open(sd, 'wb')
        except TypeError:
            showwarning(_("No output file specified"),
                        _("No processing settings entered!\n"))
        else:
            sd_file.write(output.process())
            sd_file.close()

class PreferencesDialog(tkSimpleDialog.Dialog):
    '''A dialog to change preferences and options.'''



class ErrorDialog(tkSimpleDialog.Dialog):

    def __init__(self, parent, message):
        self.message = message
        tkSimpleDialog.Dialog.__init__(self, parent)

    def body(self, master):
        title = _("Error")
        message1 = _("Connection failed with the following error message:\n")
        message2 = _("\nCheck your connection parameters and try again.\n")
        Label(master, bitmap="error", fg="red").pack()
        Label(master, text=title, font=("Helvetica", "16", "bold")).pack()
        Label(master, text=message1).pack()
        t = Entry(master, width=80)
        t.insert(END, self.message)
        t.pack()
        Label(master, text=message2).pack()

    def buttonbox(self):
        box = Frame(self)
        w = Button(box,
                   text=_("Cancel"),
                   width=10,
                   command=self.cancel,
                   default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("&lt;Return>", self.cancel)
        self.bind("&lt;Escape>", self.cancel)
        box.pack()


class Tops:

    def __init__(self, parent):

        #init user's preferences config file object
        self.upref = UserPrefs()

        buttons_width = 8
        imb_buttonx = "2m"
        imb_buttony = "1m"
        imb_buttons_framex = "3m"
        imb_buttons_framey = "2m"
        imb_int_buttons_framex = "3m"
        imb_int_buttons_framey = "1m"

        self.myParent = parent

        self.main_frame = Frame(parent) ###
        self.main_frame.pack(expand=YES, fill=BOTH)

		#MENU
        self.menubar = Menu(self.myParent)
        self.myParent.config(menu=self.menubar)

        topsmenu = Menu(self.menubar, tearoff=0)
        topsmenu.add_command(label=_("Connect"), command=self.connect)
        topsmenu.add_command(label=_("Process data"), command=self.process)
        topsmenu.add_separator()
        topsmenu.add_command(label=_("Quit"), command=self.on_app_close)

        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label=_("Open file"), command=self.open_a_file)
        filemenu.add_command(label=_("Save raw data"), command=self.save_a_file)

        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label=_("About TOPS"), command=self.about)

        languagemenu = Menu(self.menubar, tearoff=0)
        language = StringVar()
        languagemenu.add_radiobutton(label="English",variable=language,value="en")
        languagemenu.add_radiobutton(label="Italiano",variable=language,value="it")

        self.menubar.add_cascade(label="Total Station", menu=topsmenu)
        self.menubar.add_cascade(label="File", menu=filemenu)
        #self.menubar.add_cascade(label="Language", menu=languagemenu)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

        self.upper_frame = Frame(self.main_frame) ###
        self.upper_frame.pack(side=TOP, expand=NO, padx=10,
                                   pady=5, ipadx=5, ipady=5)

        self.logo_frame = Frame(self.upper_frame)
        self.logo_frame.pack(side=LEFT, expand=NO)

        self.logo_data = logo_data
        self.logo = PhotoImage(data=self.logo_data)
        self.logo_canvas = Label(self.logo_frame, image=self.logo)
        self.logo_canvas.pack(side=LEFT, expand=NO, padx=5,
                                   pady=5)

        self.header_frame = Frame(self.upper_frame)
        self.header_frame.pack(side=LEFT, expand=NO, pady=5)

        self.buttons_frame = Frame(self.header_frame)
        self.buttons_frame.pack(
            side=TOP,
            expand=NO,
            fill=Y,
            ipadx=5,
            ipady=5)

        # default control panel
        self.control_panel0 = Frame(self.header_frame)
        self.control_panel0.pack(
            side=TOP,
            expand=YES,
            fill=Y, padx=5, pady=5)

        # control panel for custom serial connection
        self.control_panel = Frame(self.header_frame)

        # option 1 : serial port
        self.option1_frame = Frame(self.control_panel0, relief=RIDGE, bd=1)
        self.option1_frame.pack(side=TOP)

        self.option1_label = Label(self.option1_frame,
                                   text=_("Port"),
                                   width=30)
        self.option1_label.pack(side=LEFT)
        self.option1_value = StringVar()
        self.option1_value.set(self.upref.getvalue('port'))

# Leave this Entry uncommented to enter port as a string, or ...
#
        self.option1_entry = Entry(self.option1_frame,
                                   textvariable=self.option1_value,
                                   width=20)

# ... comment out this Menubutton if you want to use the scan() output
#
#        self.option1_entry = Menubutton(self.option1_frame,
#                                        text="choose a value",
#                                        textvariable=self.option1_value,
#                                        relief=RAISED,
#                                        width=24)
#        self.option1_entry.menu = Menu( self.option1_entry, tearoff=0 )
#        self.option1_entry["menu"] = self.option1_entry.menu
#        for n,s in scan():
#            self.option1_entry.menu.add_radiobutton ( label=s,
#                                           variable=self.option1_value,
#                                           value = s)

        self.option1_entry.pack(side=LEFT, anchor=W)

        # option MODEL substitutes all connection parameters for better
        # user experience

        self.optionMODEL_frame = Frame(
            self.control_panel0,
            relief=RIDGE,
            bd=1)
        self.optionMODEL_frame.pack(side=TOP)

        self.optionMODEL_label = Label(self.optionMODEL_frame,
                                   text=_("Total Station"),
                                   justify=LEFT,
                                   width=30)
        self.optionMODEL_label.pack(side=LEFT, anchor=E)
        self.optionMODEL_value = StringVar()

        self.optionMODEL_value.set(self.upref.getvalue('model'))

        self.optionMODEL_entry = Menubutton(self.optionMODEL_frame,
                                        text="choose a model",
                                        textvariable=self.optionMODEL_value,
                                        relief=RAISED,
                                        width=20)
        self.optionMODEL_entry.menu = Menu(self.optionMODEL_entry, tearoff=0)
        self.optionMODEL_entry["menu"] = self.optionMODEL_entry.menu

        for k, (l, m, n) in BUILTIN_MODELS.items():
            self.optionMODEL_entry.menu.add_radiobutton(
                label=n,
                variable=self.optionMODEL_value,
                value=k,
                command=self.print_model)
        self.optionMODEL_entry.pack(side=LEFT, anchor=W)

        # option 2 : baudrate
        self.option2_frame = Frame(self.control_panel, relief=RIDGE, bd=1)
        self.option2_frame.pack(side=TOP)

        self.option2_label = Label(self.option2_frame,
                                   text="Baudrate",
                                   width=30)
        self.option2_label.pack(side=LEFT)
        self.option2_value = IntVar()

        try:
            assert serial.baudrate_constants
            assert serial.baudrate_constants is not {}
        except (AttributeError, AssertionError):
            self.option2_entry = Entry(self.option2_frame,
                                       textvariable=self.option2_value,
                                       width=20)
        else:
            self.option2_entry = Menubutton(self.option2_frame,
                                            text=_("choose a value"),
                                            textvariable=self.option2_value,
                                            relief=RAISED,
                                            width=20)
            self.option2_entry.menu = Menu(self.option2_entry, tearoff=0)
            self.option2_entry["menu"] = self.option2_entry.menu
            for key in sorted(serial.baudrate_constants.keys()): # dynamic list
                self.option2_entry.menu.add_radiobutton(
                    label="%s" % key,
                    variable=self.option2_value,
                    value=key,
                    )
        self.option2_entry.pack(side=LEFT, anchor=W)

        # option 3 : bytesize
        self.option3_frame = Frame(self.control_panel, relief=RIDGE, bd=1)
        self.option3_frame.pack(side=TOP)

        self.option3_label = Label(self.option3_frame,
                                   text=_("Bytesize"),
                                   justify=LEFT,
                                   width=30)
        self.option3_label.pack(side=LEFT, anchor=E)
        self.option3_value = IntVar()
        self.option3_entry = Menubutton(self.option3_frame,
                                        text=_("choose a value"),
                                        textvariable=self.option3_value,
                                        relief=RAISED,
                                        width=20)
        self.option3_entry.menu = Menu(self.option3_entry, tearoff=0)
        self.option3_entry["menu"] = self.option3_entry.menu
        for v in [8,7,6,5]:
            self.option3_entry.menu.add_radiobutton(label=str(v),
                                                    variable=self.option3_value,
                                                    value=v)
        self.option3_entry.pack(side=LEFT, anchor=W)

        # option 4 : parity
        self.option4_frame = Frame(self.control_panel, relief=RIDGE, bd=1)
        self.option4_frame.pack(side=TOP)

        self.option4_label = Label(self.option4_frame,
                                   text=_("Parity setting"),
                                   justify=LEFT,
                                   width=30)
        self.option4_label.pack(side=LEFT, anchor=E)
        self.option4_value = StringVar()
        self.option4_entry = Menubutton(self.option4_frame,
                                        text=_("choose a value"),
                                        textvariable=self.option4_value,
                                        relief=RAISED,
                                        width=20)
        self.option4_entry.menu = Menu(self.option4_entry, tearoff=0)
        self.option4_entry["menu"] = self.option4_entry.menu
        for v in ['Even', 'None', 'Odd']:
            self.option4_entry.menu.add_radiobutton(label=_(v),
                                                    variable=self.option4_value,
                                                    value=v[0])
        self.option4_entry.pack(side=LEFT, anchor=W)

        # option 5 : stop bit
        self.option5_frame = Frame(self.control_panel, relief=RIDGE, bd=1)
        self.option5_frame.pack(side=TOP)

        self.option5_label = Label(self.option5_frame,
                                   text=_("Stop bit"),
                                   justify=LEFT,
                                   width=30)
        self.option5_label.pack(side=LEFT, anchor=E)
        self.option5_value = IntVar()
        self.option5_entry = Menubutton(self.option5_frame,
                                        text=_("choose a value"),
                                        textvariable=self.option5_value,
                                        relief=RAISED,
                                        width=20)
        self.option5_entry.menu = Menu(self.option5_entry, tearoff=0)
        self.option5_entry["menu"] = self.option5_entry.menu
        for v in [1, 2]:
            self.option5_entry.menu.add_radiobutton(label=str(v),
                                                    variable=self.option5_value,
                                                    value=v)
        self.option5_entry.pack(side=LEFT, anchor=W)

        # option 6 : time lapse between data packets
        self.option6_frame = Frame(self.control_panel, relief=RIDGE, bd=1)
        self.option6_frame.pack(side=TOP)

        self.option6_label = Label(self.option6_frame,
                                   text=_("Time lapse between data packets"),
                                   justify=LEFT,
                                   width=30)
        self.option6_label.pack(side=LEFT, anchor=E)
        self.option6_value = DoubleVar()
        self.option6_value.set(self.upref.getvalue('sleeptime'))
        self.option6_entry = Entry(self.option6_frame,
                                   textvariable=self.option6_value,
                                   relief=RAISED,
                                   justify=RIGHT,
                                   width=20)
        self.option6_entry.pack(side=LEFT, anchor=W)

        # control buttons

        self.connect_button = Button(self.buttons_frame,
                                      text=_("Connect"),
                                      padx=imb_buttonx,
                                      pady=imb_buttony)
        self.connect_button.pack(side=LEFT, anchor=S)
        self.connect_button.bind("<Button-1>", self.connect_action)
        self.connect_button.bind("<Return>", self.connect_action)

        self.save_button = Button(self.buttons_frame,
                                      text=_("Save raw data"),
                                      padx=imb_buttonx,
                                      pady=imb_buttony)
        self.save_button.pack(side=LEFT, anchor=S)
        self.save_button.bind("<Button-1>", self.save_action)
        self.save_button.bind("<Return>", self.save_action)

        self.process_button = Button(self.buttons_frame,
                                     text=_("Process data"),
                                     padx=imb_buttonx,
                                     pady=imb_buttony)
        self.process_button.pack(side=LEFT, anchor=S)
        self.process_button.bind("<Button-1>", self.process_action)
        self.process_button.bind("<Return>", self.process_action)

        self.status = StatusBar(self.main_frame)
        self.status.set('Welcome to Total Open Station')
        self.status.pack(side=BOTTOM, fill=X)

        # text frame
        self.text_frame = Frame(self.main_frame)
        self.text_frame.pack(side=BOTTOM, expand=YES, fill=BOTH)

        self.text_area = Text(self.text_frame, width=80)
        self.text_area.insert(END, _("Welcome.\nTurn your device on."))
        self.text_area.pack(side=LEFT, expand=YES, fill=Y)

        self.scrollY = Scrollbar(self.text_frame,
                                 orient=VERTICAL,
                                 command=self.text_area.yview)
        self.text_area['yscrollcommand'] = self.scrollY.set
        self.scrollY.pack(side=RIGHT, expand=YES, fill=Y, anchor=W)

        # init stuff
        self.myParent.title("Total Open Station")
        self.myParent.protocol("WM_DELETE_WINDOW", self.on_app_close)
        self.print_model()
        self.myParent.mainloop()

    def on_click_language(self):
        '''
            open select language dialog
        '''
        pass

    def on_app_close(self):
        '''Callback function to ask confirmation before quitting the application.'''

        if askokcancel("Quit","Do you really want to quit application ?"):
            self.myParent.destroy()

    def exit_action(self, event):
        self.on_app_close()

    def print_model(self):
        model = self.optionMODEL_value.get()
        if model != 'custom':
            self.control_panel.forget()
            self.option2_value.set(0)
            self.option3_value.set(0)
            self.option4_value.set('')
            self.option5_value.set(0)
        else:
            self.option2_value.set(9600)
            self.option3_value.set(8)
            self.option4_value.set('N')
            self.option5_value.set(1)
            self.control_panel.pack(side=TOP,
                                    expand=YES,
                                    fill=Y,
                                    ipadx=5,
                                    ipady=5)

    def connect(self):

        chosen_model = self.optionMODEL_value.get()
        chosen_port = self.option1_value.get()

        # do nothing if input is empty
        if not (chosen_model == '' or chosen_port == ''):

            if chosen_model == 'custom':

                # dictionary for passing options to Serial
                self.options = {'baudrate': self.option2_value.get(),
                                'bytesize': self.option3_value.get(),
                                'parity': self.option4_value.get(),
                                'stopbits': self.option5_value.get()}
            else:
                self.options = {}

            modelclass = BUILTIN_MODELS[chosen_model]
            if isinstance(modelclass, tuple):
                try:
                    # builtin model builder
                    mod, cls, name = modelclass
                    modelclass = getattr(
                        __import__('totalopenstation.models.' + mod, None, None, [cls]), cls)
                except ImportError, msg:
                    showwarning(_('Import error'),
                                _('Error loading the required model module: %s' % msg))

                mc = modelclass(chosen_port, **self.options)

                try:
                    mc.close()  # sometimes the port will be already open for no reason
                    mc.open()
                except serial.SerialException, detail:
                    e = ErrorDialog(self.myParent, detail)
                else:
                    st = DownloadDialog(self.myParent)
                    sleeptime = self.option6_value.get()
                    if st.result:
                        self.status.set(_("Waiting for data: please start transfer from your total station menu."))
                        while mc.inWaiting() == 0:
                            sleep(sleeptime)
                        n = mc.inWaiting()
                        result = mc.read(n)
                        self.replace_text(str(result))
                        sleep(sleeptime)

                        while mc.inWaiting() > 0:
                            newdata = mc.read(mc.inWaiting())
                            result += newdata
                            self.status.set(_('Downloaded %d bytes'), len(result))
                            self.replace_text(str(result))
                            sleep(sleeptime) # TODO determine sleep time from baudrate
                        mc.close()
                        showinfo(_('Success!'),
                                 _('Download finished!\nYou have %d bytes of data.') % len(result))

    def connect_action(self, event):
        self.connect()

    def open_a_file(self):
        try:
            d = tkFileDialog.askopenfilename()
            of = open(d, 'r')
            oc = of.read()
            self.replace_text(oc)
        except:
            pass

    def open_action(self, event):
        self.open_a_file()

    def process(self):
        data = self.text_area.get("1.0", END)
        d = ProcessDialog(self.myParent, data)

    def process_action(self, event):
        self.process()

    def save_a_file(self):
        try:
            sd = tkFileDialog.asksaveasfilename(defaultextension='.tops')
            data = self.text_area.get("1.0", END)
            of = open(sd, 'w')
            oc = of.write(data)
        except:
            pass

    def save_action(self, event):
        self.save_a_file()

    def about(self):
        d = AboutDialog(self.myParent)

    def about_action(self, event):
        self.about()

    def replace_text(self, text):
        self.text_area.delete("1.0", END)
        self.text_area.insert(END, text.replace('\r', ''))
        self.text_area.yview_moveto(1.0)
        self.text_area.update_idletasks()


root = Tk()
Tops = Tops(root)


#save user's preferences (model, port and sleeptime if custom model)

atexit.register(Tops.upref.setvalues,
                {'model': Tops.optionMODEL_value.get(),
                 'port': Tops.option1_value.get(),
                 'sleeptime': Tops.option6_value.get(),
                 })
