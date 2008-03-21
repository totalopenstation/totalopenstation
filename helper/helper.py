#! /usr/bin/env python
# -*- coding: utf-8 -*-

import serial

from Tkinter import *

class MiaApp:
  def __init__(self, genitore):

    #--- costanti per il controllo della disposizione
    #--- dei pulsanti
    larghezza_pulsanti = 8
    imb_pulsantex = "2m"
    imb_pulsantey = "1m"
    imb_quadro_pulsantix = "3m"
    imb_quadro_pulsantiy = "2m"
    imb_int_quadro_pulsantix = "3m"
    imb_int_quadro_pulsantiy = "1m"

    self.mioGenitore = genitore

    ### Il quadro principale si chiama 'quadro_grande'
    self.quadro_grande = Frame(genitore) ###
    self.quadro_grande.pack(expand = YES, fill = BOTH)

    # 'quadro_controllo' - praticamente tutto tranne la
    # dimostrazione
    self.quadro_controllo = Frame(self.quadro_grande) ###
    self.quadro_controllo.pack(side = TOP, expand = NO, padx = 10,
                               pady = 5, ipadx = 5, ipady = 5)

    # All'interno di 'quadro_controllo' si creano un'etichetta
    # per il titolo e un 'quadro_pulsanti'
    
    self.header_frame = Frame(self.quadro_controllo)
    self.header_frame.pack(side = TOP, expand = NO)

    self.logo = PhotoImage(file = "total-station.gif")
    
    self.logo_canvas = Label(self.header_frame, image=self.logo)
    self.logo_canvas.pack(side = LEFT, expand = NO)

    mioMessaggio = """
    This program will help you to find the right connection
    parameters for your total station device, and after that also to retrieve
    data from it."""
    Label(self.header_frame,
      text = mioMessaggio,
      justify = LEFT).pack(side = LEFT, anchor = W)
    


    # 'quadro_pulsanti'
    self.quadro_pulsanti = Frame(self.quadro_controllo)
    self.quadro_pulsanti.pack(side = TOP, expand = NO, fill = Y,
                              ipadx = 5, ipady = 5)

    # 'quadro_dimostrativo'
    self.quadro_dimostrativo = Frame(self.quadro_grande)
    self.quadro_dimostrativo.pack(side = TOP, expand = YES,
                                  fill = BOTH)
    
    # text frame
    self.text_frame = Frame(self.quadro_grande)
    self.text_frame.pack(side = BOTTOM, expand = YES, fill = BOTH)
    
    self.text_area = Text(self.text_frame, width = 80)
    self.text_area.insert(END, "hello,\nsilly boy.\nturn your device on.")
    self.text_area.pack(side = LEFT, expand = YES, fill = Y)
    
    self.scrollY = Scrollbar ( self.text_frame, orient=VERTICAL,
    command=self.text_area.yview )
    self.text_area['yscrollcommand'] = self.scrollY.set

    self.scrollY.pack(side = RIGHT,expand = YES, fill = Y, anchor = W)
    
    # control panel
    self.control_panel = Frame(self.quadro_grande)
    self.control_panel.pack(side = TOP, expand = YES, fill = Y, ipadx = 5)
    
    # option 1 : serial port
    self.option1_frame = Frame(self.control_panel, relief = RIDGE, bd = 1)
    self.option1_frame.pack(side = TOP)
    
    self.option1_label = Label(self.option1_frame,
                               text="Port",
                               width = 25).pack(side = LEFT)
    self.option1_value = StringVar()
    self.option1_value.set("/dev/ttyUSB0")
    self.option1_entry = Entry(self.option1_frame,
                               textvariable=self.option1_value,
                               width = 25)
    self.option1_entry.pack(side = LEFT, anchor = W)
    
    # option 2 : baudrate
    self.option2_frame = Frame(self.control_panel, relief = RIDGE, bd = 1)
    self.option2_frame.pack(side = TOP)
    
    self.option2_label = Label(self.option2_frame,
                               text="Baudrate",
                               width = 25).pack(side = LEFT)
    self.option2_value = IntVar()
    self.option2_value.set(9600)
    self.option2_entry = Menubutton(self.option2_frame,
                                    text="choose a value",
                                    relief = RAISED,
                                    width = 24)
    self.option2_entry.menu =   Menu ( self.option2_entry, tearoff=0 )
    self.option2_entry["menu"]  = self.option2_entry.menu
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
                               width = 25).pack(side = LEFT, anchor = E)
    self.option3_value = IntVar()
    self.option3_entry = Menubutton(self.option3_frame,
                                    text="choose a value",
                                    relief = RAISED,
                                    width = 24)
    self.option3_entry.menu =   Menu ( self.option3_entry, tearoff=0 )
    self.option3_entry["menu"]  = self.option3_entry.menu
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
                               width = 25).pack(side = LEFT, anchor = E)
    self.option4_value = StringVar()
    self.option4_entry = Menubutton(self.option4_frame,
                                    text="choose a value",
                                    relief = RAISED,
                                    width = 24)
    self.option4_entry.menu =   Menu ( self.option4_entry, tearoff=0 )
    self.option4_entry["menu"]  = self.option4_entry.menu
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
                               width = 25).pack(side = LEFT, anchor = E)
    self.option5_value = IntVar()
    self.option5_entry = Menubutton(self.option5_frame,
                                    text="choose a value",
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
                               text="Timeout",
                               justify = LEFT,
                               width = 25).pack(side = LEFT, anchor = E)
    self.option6_value = StringVar()
    self.option6_value.set("type value, empty for None") 
    self.option6_entry = Entry(self.option6_frame,
                               textvariable=self.option6_value,
                               width = 25)
    self.option6_entry.pack(side = LEFT, anchor = W)
    
    # option 7 : xon/xoff
    self.option7_frame = Frame(self.control_panel, relief = RIDGE, bd = 1)
    self.option7_frame.pack(side = TOP)
    
    self.option7_label = Label(self.option7_frame,
                               text="Xon/Xoff flow control",
                               justify = LEFT,
                               width = 25).pack(side = LEFT, anchor = E)
    self.option7_value = IntVar()
    self.option7_entry = Menubutton(self.option7_frame,
                                    text="choose a value",
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
                               width = 25).pack(side = LEFT, anchor = E)
    self.option8_value = IntVar()
    self.option8_entry = Menubutton(self.option8_frame,
                                    text="choose a value",
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
    
    # Si aggiungono alcuni sottoquadri a 'quadro_pulsanti'
    self.quadro_nomi_pulsanti = Frame(self.quadro_pulsanti,
                                      borderwidth = 5)

    self.quadro_nomi_pulsanti.pack(side = LEFT, expand = YES,
                                   fill = Y, anchor = N)

    self.quadroPulsanteAnnulla = Frame(self.quadro_nomi_pulsanti)
    self.quadroPulsanteAnnulla.pack(side = BOTTOM, 
                                    expand = YES, 
                                    anchor = SW)

    self.pulsanteAnnulla = Button(self.quadroPulsanteAnnulla,
                                  text = "Exit", 
                                  background = "red", 
                                  width = larghezza_pulsanti, 
                                  padx = imb_pulsantex, 
                                  pady = imb_pulsantey)
    self.pulsanteAnnulla.pack(side = LEFT, anchor = S)
    
    self.connect_button = Button(self.quadroPulsanteAnnulla,
                                  text = "Connect",
                                  background = "green",
                                  width = larghezza_pulsanti,
                                  padx = imb_pulsantex, 
                                  pady = imb_pulsantey)
    self.connect_button.pack(side = LEFT, anchor = S)

    self.pulsanteAnnulla.bind("<Button-1>", 
      self.pulsanteAnnullaPremuto)
    self.pulsanteAnnulla.bind("<Return>", 
      self.pulsanteAnnullaPremuto)

  def pulsanteAnnullaPremuto(self, evento):
      self.mioGenitore.destroy()


radice = Tk()
miaApp = MiaApp(radice)
radice.title("Total Open Station helper")
radice.mainloop()
