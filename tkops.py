#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tkops.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import serial

from time import sleep

from Tkinter import *
import tkSimpleDialog

def scan():
    """scan for available ports. return a list of tuples (num, name).
    
    Part of pySerial (http://pyserial.sf.net)  (C)2002-2003 <cliechti@gmx.net>
    """
    available = []
    for i in range(256):
        try:
            s = serial.Serial(i)
            available.append( (i, s.portstr))
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


class AboutDialog(tkSimpleDialog.Dialog):
    def body(self, master):
        title="Total Open Station 0.1"
        message="""
Total Open Station is copyright 2008 Luca Bianconi, Stefano Costa and the IOSA
project.

http://totalopenstation.sharesource.org/

The application logo is copyright 2008 Lapo Calamandrei."""
        
        self.logo_data = logo_data
        self.logo = PhotoImage(data = self.logo_data)
        Label(master, image=self.logo).pack()
        
        Label(master, text=title, font=("Helvetica", "16", "bold")).pack()
        Label(master, text=message).pack()
    
    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.cancel, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("&lt;Return>", self.cancel)
        self.bind("&lt;Escape>", self.cancel)
        box.pack()


class ConnectDialog(tkSimpleDialog.Dialog):
    def __init__(self, parent, cs):
        self.conn_str = cs
        tkSimpleDialog.Dialog.__init__(self, parent)
    
    def body(self, master):
        title="waiting for data from device"
        message1="Connection initialized with the following parameters:\n"
        params = "%s\n" %(self.conn_str)
        message2 = "\nStart the download procedure on the device.\n"
        message2 = message2 + "Press OK when done."
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
        tkSimpleDialog.Dialog.__init__(self, parent)
    
    def body(self, master):
        title="Choose output format and destination file"
        question = "Output format:\n"

        message1="Data to be processed:\n"
        params = "%s\n" %(self.data)
        Label(master, bitmap="question").pack()
        Label(master, text=title, font=("Helvetica", "16", "bold")).pack()
        Label(master, text=question).pack()
        output_format = StringVar()
        for t in ['CSV', 'DAT', 'DXF']:
            w = Radiobutton(master,
                            text = t,
                            value = t,
                            variable = output_format
                            ).pack()
        Label(master, text=message1).pack()
        t = Text(master,
             width=80)
        t.insert(END, params)
        t.pack()


class ErrorDialog(tkSimpleDialog.Dialog):
    def __init__(self, parent, message):
        self.message = message
        tkSimpleDialog.Dialog.__init__(self, parent)
    
    def body(self, master):
        title="Error"
        message1="Connection failed with the following error message:\n"
        message2 = "\nCheck your connection parameters and try again.\n"
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
                   text="Cancel",
                   width=10,
                   command=self.cancel,
                   default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("&lt;Return>", self.cancel)
        self.bind("&lt;Escape>", self.cancel)
        box.pack()


class Tops:
    def __init__(self, parent):

        #--- costanti per il controllo della disposizione
        #--- dei pulsanti
        buttons_width = 8
        imb_buttonx = "2m"
        imb_buttony = "1m"
        imb_buttons_framex = "3m"
        imb_buttons_framey = "2m"
        imb_int_buttons_framex = "3m"
        imb_int_buttons_framey = "1m"

        self.myParent = parent

        self.main_frame = Frame(parent) ###
        self.main_frame.pack(expand = YES, fill = BOTH)

        self.upper_frame = Frame(self.main_frame) ###
        self.upper_frame.pack(side = TOP, expand = NO, padx = 10,
                                   pady = 5, ipadx = 5, ipady = 5)

        self.header_frame = Frame(self.upper_frame)
        self.header_frame.pack(side = TOP, expand = NO)
        
        self.logo_data = logo_data
        self.logo = PhotoImage(data = self.logo_data)
        
        self.logo_canvas = Label(self.header_frame, image=self.logo)
        self.logo_canvas.pack(side = LEFT, expand = NO)

        welcome_message = """
        This program will help you to find the right connection
        parameters for your total station device, and after that also
        to retrieve data from it."""
        Label(self.header_frame,
          text = welcome_message,
          justify = LEFT).pack(side = LEFT, anchor = W)
        
        self.buttons_frame = Frame(self.upper_frame)
        self.buttons_frame.pack(side = TOP, expand = NO, fill = Y,
                                  ipadx = 5, ipady = 5)
        
        # control panel
        self.control_panel = Frame(self.main_frame)
        self.control_panel.pack(side = TOP, expand = YES, fill = Y, ipadx = 5)
        
        # option 1 : serial port
        self.option1_frame = Frame(self.control_panel, relief = RIDGE, bd = 1)
        self.option1_frame.pack(side = TOP)
        
        self.option1_label = Label(self.option1_frame,
                                   text="Port",
                                   width = 25)
        self.option1_label.pack(side = LEFT)
        self.option1_value = StringVar()
        self.option1_entry = Entry(self.option1_frame,
                                   textvariable=self.option1_value,
                                   width = 25)
#        self.option1_entry = Menubutton(self.option1_frame,
#                                        text="choose a value",
#                                        textvariable=self.option1_value,
#                                        relief = RAISED,
#                                        width = 24)
#        self.option1_entry.menu = Menu( self.option1_entry, tearoff=0 )
#        self.option1_entry["menu"] = self.option1_entry.menu
#        for n,s in scan():
#            self.option1_entry.menu.add_radiobutton ( label=s,
#                                           variable=self.option1_value,
#                                           value = n)
        self.option1_entry.pack(side = LEFT, anchor = W)
        
        # option 2 : baudrate
        self.option2_frame = Frame(self.control_panel, relief = RIDGE, bd = 1)
        self.option2_frame.pack(side = TOP)
        
        self.option2_label = Label(self.option2_frame,
                                   text="Baudrate",
                                   width = 25)
        self.option2_label.pack(side = LEFT)
        self.option2_value = IntVar()
        self.option2_value.set(9600)
        self.option2_entry = Menubutton(self.option2_frame,
                                        text="choose a value",
                                        textvariable=self.option2_value,
                                        relief = RAISED,
                                        width = 24)
        self.option2_entry.menu = Menu( self.option2_entry, tearoff=0 )
        self.option2_entry["menu"] = self.option2_entry.menu
        self.option2_entry.menu.add_radiobutton ( label="9600",
                                       variable=self.option2_value,
                                       value = 9600 )
        self.option2_entry.menu.add_radiobutton ( label="4800",
                                       variable=self.option2_value,
                                       value = 4800 )
        self.option2_entry.pack(side = LEFT, anchor = W)
        
        # option 3 : bytesize
        self.option3_frame = Frame(self.control_panel, relief = RIDGE, bd = 1)
        self.option3_frame.pack(side = TOP)
        
        self.option3_label = Label(self.option3_frame,
                                   text="Bytesize",
                                   justify = LEFT,
                                   width = 25)
        self.option3_label.pack(side = LEFT, anchor = E)
        self.option3_value = IntVar()
        self.option3_value.set(8)
        self.option3_entry = Menubutton(self.option3_frame,
                                        text="choose a value",
                                        textvariable=self.option3_value,
                                        relief = RAISED,
                                        width = 24)
        self.option3_entry.menu = Menu( self.option3_entry, tearoff=0 )
        self.option3_entry["menu"] = self.option3_entry.menu
        self.option3_entry.menu.add_radiobutton (label="8",
                                                 variable=self.option3_value,
                                                 value = 8 )
        self.option3_entry.menu.add_radiobutton (label="7",
                                                 variable=self.option3_value,
                                                 value = 7 )
        self.option3_entry.menu.add_radiobutton (label="6",
                                                 variable=self.option3_value,
                                                 value = 6 )
        self.option3_entry.menu.add_radiobutton (label="5",
                                                 variable=self.option3_value,
                                                 value = 5 )
        self.option3_entry.pack(side = LEFT, anchor = W)
        
        # option 4 : parity
        self.option4_frame = Frame(self.control_panel, relief = RIDGE, bd = 1)
        self.option4_frame.pack(side = TOP)
        
        self.option4_label = Label(self.option4_frame,
                                   text="Parity setting",
                                   justify = LEFT,
                                   width = 25)
        self.option4_label.pack(side = LEFT, anchor = E)
        self.option4_value = StringVar()
        self.option4_value.set('N')
        self.option4_entry = Menubutton(self.option4_frame,
                                        text="choose a value",
                                        textvariable=self.option4_value,
                                        relief = RAISED,
                                        width = 24)
        self.option4_entry.menu = Menu( self.option4_entry, tearoff=0 )
        self.option4_entry["menu"] = self.option4_entry.menu
        self.option4_entry.menu.add_radiobutton (label="Even",
                                                 variable=self.option4_value,
                                                 value = "E" )
        self.option4_entry.menu.add_radiobutton (label="None",
                                                 variable=self.option4_value,
                                                 value = "N" )
        self.option4_entry.menu.add_radiobutton (label="Odd",
                                                 variable=self.option4_value,
                                                 value = "O" )
        self.option4_entry.pack(side = LEFT, anchor = W)
        
        # option 5 : stop bit
        self.option5_frame = Frame(self.control_panel, relief = RIDGE, bd = 1)
        self.option5_frame.pack(side = TOP)
        
        self.option5_label = Label(self.option5_frame,
                                   text="Stop bit",
                                   justify = LEFT,
                                   width = 25)
        self.option5_label.pack(side = LEFT, anchor = E)
        self.option5_value = IntVar()
        self.option5_value.set(1)
        self.option5_entry = Menubutton(self.option5_frame,
                                        text="choose a value",
                                        textvariable=self.option5_value,
                                        relief = RAISED,
                                        width = 24)
        self.option5_entry.menu =   Menu ( self.option5_entry, tearoff=0 )
        self.option5_entry["menu"]  = self.option5_entry.menu
        self.option5_entry.menu.add_radiobutton (label="1",
                                                 variable=self.option5_value,
                                                 value = 1 )
        self.option5_entry.menu.add_radiobutton (label="2",
                                                 variable=self.option5_value,
                                                 value = 2 )
        self.option5_entry.pack(side = LEFT, anchor = W)

        # option 6 : timeout
        self.option6_frame = Frame(self.control_panel, relief = RIDGE, bd = 1)
        self.option6_frame.pack(side = TOP)
        
        self.option6_label = Label(self.option6_frame,
                                   text="Timeout (empty for None)",
                                   justify = LEFT,
                                   width = 25)
        self.option6_label.pack(side = LEFT, anchor = E)
        self.option6_value = StringVar()
        self.option6_value.set("0") 
        self.option6_entry = Entry(self.option6_frame,
                                   textvariable=self.option6_value,
                                   width = 25)
        self.option6_entry.pack(side = LEFT, anchor = W)
        
        # option 7 : xonxoff
        self.option7_frame = Frame(self.control_panel, relief = RIDGE, bd = 1)
        self.option7_frame.pack(side = TOP)
        
        self.option7_label = Label(self.option7_frame,
                                   text="Xon/Xoff flow control",
                                   justify = LEFT,
                                   width = 25)
        self.option7_label.pack(side = LEFT, anchor = E)
        self.option7_value = IntVar()
        self.option7_entry = Menubutton(self.option7_frame,
                                        text="choose a value",
                                        textvariable=self.option7_value,
                                        relief = RAISED,
                                        width = 24)
        self.option7_entry.menu =   Menu ( self.option7_entry, tearoff=0 )
        self.option7_entry["menu"]  = self.option7_entry.menu
        self.option7_entry.menu.add_radiobutton (label="Enabled",
                                                 variable=self.option7_value,
                                                 value = 1 )
        self.option7_entry.menu.add_radiobutton (label="Disabled",
                                                 variable=self.option7_value,
                                                 value = 0 )
        self.option7_entry.pack(side = LEFT, anchor = W)
        
        # option 8: hardware flow control
        self.option8_frame = Frame(self.control_panel, relief = RIDGE, bd = 1)
        self.option8_frame.pack(side = TOP)
        
        self.option8_label = Label(self.option8_frame,
                                   text="Hardware flow control",
                                   justify = LEFT,
                                   width = 25)
        self.option8_label.pack(side = LEFT, anchor = E)
        self.option8_value = IntVar()
        self.option8_entry = Menubutton(self.option8_frame,
                                        text="choose a value",
                                        textvariable=self.option8_value,
                                        relief = RAISED,
                                        width = 24)
        self.option8_entry.menu =   Menu ( self.option8_entry, tearoff=0 )
        self.option8_entry["menu"]  = self.option8_entry.menu
        self.option8_entry.menu.add_radiobutton (label="Enabled",
                                                 variable=self.option8_value,
                                                 value = 1 )
        self.option8_entry.menu.add_radiobutton (label="Disabled",
                                                 variable=self.option8_value,
                                                 value = 0 )
        self.option8_entry.pack(side = LEFT, anchor = W)
    
        # dictionary for passing options to Serial
        self.options = {'port':(1,'str'),
                   'baudrate':(2,'int'),
                   'bytesize':(3,'int'),
                   'parity':(4,'str'),
                   'stopbits':(5,'int'),
                   'timeout':(6,'int'),
                   'xonxoff':(7,'bool'),
                   'rtscts':(8,'bool')}
        
        # control buttons
        self.exit_button = Button(self.buttons_frame,
                                      text = "Quit", 
                                      width = buttons_width, 
                                      padx = imb_buttonx, 
                                      pady = imb_buttony)
        self.exit_button.pack(side = LEFT, anchor = S)
        self.exit_button.bind("<Button-1>", self.exit_action)
        self.exit_button.bind("<Return>", self.exit_action)
        
        self.connect_button = Button(self.buttons_frame,
                                      text = "Connect",
                                      background = "green",
                                      width = buttons_width,
                                      padx = imb_buttonx, 
                                      pady = imb_buttony)
        self.connect_button.pack(side = LEFT, anchor = S)
        self.connect_button.bind("<Button-1>", self.connect_action)
        self.connect_button.bind("<Return>", self.connect_action)
        
        self.process_button = Button(self.buttons_frame,
                                        text = "Process data",
                                        background = "cyan",
                                        padx = imb_buttonx,
                                        pady = imb_buttony)
        self.process_button.pack(side = LEFT, anchor = S)
        self.process_button.bind("<Button-1>", self.process_action)
        self.process_button.bind("<Return>", self.process_action)
        
        self.about_button = Button(self.buttons_frame,
                                      text = "About TOPS",
                                      padx = imb_buttonx, 
                                      pady = imb_buttony)
        self.about_button.pack(side = LEFT, anchor = S)
        self.about_button.bind("<Button-1>", self.about_action)
        self.about_button.bind("<Return>", self.about_action)
        
        # text frame
        self.text_frame = Frame(self.main_frame)
        self.text_frame.pack(side = BOTTOM, expand = YES, fill = BOTH)
        
        self.text_area = Text(self.text_frame, width = 80)
        self.text_area.insert(END, "Welcome.\nTurn your device on.")
        self.text_area.pack(side = LEFT, expand = YES, fill = Y)
        
        self.scrollY = Scrollbar ( self.text_frame, orient=VERTICAL,
        command=self.text_area.yview )
        self.text_area['yscrollcommand'] = self.scrollY.set
        self.scrollY.pack(side = RIGHT,expand = YES, fill = Y, anchor = W)
        
    def exit_action(self, event):
        self.myParent.destroy()
    
    def connect_action(self, event):
        cs = "serial.Serial("
        
        for k,v in self.options.items():
            print k,v
            n, t = v
            cs = cs + "%s = " %k
            if t == 'str':
                cs = cs + "'" + eval("self.option%s_value.get()" %n) + "'"
            elif t == 'int':
                try:
                    int(eval("self.option%s_value.get()" %n))
                except ValueError:
                    cs = cs + "None"
                else:
                    cs = cs + str(int(eval("self.option%s_value.get()" %n)))
            elif t == 'bool':
                cs = cs + str(bool(eval("self.option%s_value.get()" %n)))
            
            cs = cs + ", "
        connection_string = cs[:-2] + ")" # remove last ", "
        try:
            TOPSerial = eval(connection_string)
        except serial.SerialException, detail:
            e = ErrorDialog(self.myParent, detail)
        else:
            TOPSerial.open()
            d = ConnectDialog(self.myParent, connection_string)
            n = TOPSerial.inWaiting()
            result = TOPSerial.read(n)
            sleep(0.1)
            
            # prevent full buffer effect
            while TOPSerial.inWaiting() > 0:
                result = result + TOPSerial.read(TOPSerial.inWaiting())
                sleep(0.1)
            
            self.text_area.delete("1.0",END)
            result_to_print = result.replace('\r','')
            self.text_area.insert(END,result_to_print)
    
    def process_action(self, event):
        data = self.text_area.get("1.0", END)
        d = ProcessDialog(self.myParent, data)
    
    def about_action(self, event):
        d = AboutDialog(self.myParent)

root = Tk()
Tops = Tops(root)
root.title("Total Open Station")
root.mainloop()

