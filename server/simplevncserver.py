#!/usr/bin/python3

import subprocess
import sys
import PySimpleGUI as sg

import os
from pyvncs.lib import log

from enum import Enum

#the states of the server
class Status(Enum):

    RUNNING = 1
    STOPPED = 2

#   function that is used to stop the server
#   or to print throw an error
def stop_server():
    try:

        if status == Status.RUNNING:
            server.terminate()

    except:
        log.debug("Stopping server error")

logo = os.path.abspath("simplevnc.png")

if not os.path.exists(logo):
    logo = ""

#the basic status of the server is stopped
status = Status.STOPPED


if sys.platform in ['win32', 'win64']:

    from pyvncs.lib.oshelpers import windows as win32

    if not win32.is_admin():
        ret = win32.run_as_admin(show_console=False)
        if ret is None:
            # Respawning with admin rights
            sys.exit(0)
        elif ret is True:
            # admin rights
            pass
        else:
            print('Error(ret=%d): cannot elevate privilege.' % (ret))
            sys.exit(1)

# First the window layout in 2 columns

parameter_list_column = [

    [
        sg.Text("Server Parameters")
    ],

    #Creating the port text box
    [
        sg.Text("Port", expand_x = True),

        sg.In(size = (25, 1), enable_events = True, key = "-PORT-")
    ],

    #Creating the password text box
    #The password will not show in clear text, but will print stars
    [
        sg.Text("Password", expand_x = True),

        sg.In(size = (25, 1), enable_events = True, key = "-PASSWORD-", password_char = '*')
    ],

    #Buttons for starting and stopping the server
    [
        sg.Button(button_text = "Start Server", button_color = "#275DA4", size = 11, key = "-START-"),

        sg.Button(button_text = "Stop Server", button_color = "red", size = 11, key = "-STOP-")
    ],

    #The status of the server, base case is STOPPED
    [
        sg.Text("Status: "),

        sg.Text("STOPPED", expand_y = True, text_color = "red", key = "-STATUS-")
    ],

    #Quit button
    [
        sg.Text(" ", expand_x=True),

        sg.Button(button_text = "Quit", button_color = "#808080", key = "-QUIT-")
    ]
]


# Show the logo

image_viewer_column = [

    [sg.Image(key = "-IMAGE-", filename = logo)]

]


# ----- Full layout -----

layout = [

    [

        sg.Column(image_viewer_column),

        sg.VSeperator(),

        sg.Column(parameter_list_column)
    ]

]


window = sg.Window("SimpleVNC Server", layout)


# Run the Event Loop

while True:

    event, values = window.read()

    if event == "-QUIT-" or event == sg.WIN_CLOSED:
        stop_server()
        break

    # Actual interface logic
    # Check the event that will happen in the server

    if event == "-START-":

        stop_server() # in case the server is restarted with the same button

        # Surround the next code with try and except to check for errors
        try:
            server = subprocess.Popen([sys.executable, 'pyvncs/vncserver.py', '-P', password, '-p', port])

            window["-STATUS-"].update(value = "RUNNING", text_color = "#5DF455")
            window["-START-"].update(text = "Restart Server")

            # Changing the server status to running
            status = Status.RUNNING

        except:
            log.debug("Starting server error")
            pass

    #Stopping the server
    elif event == "-STOP-":

        window["-STATUS-"].update(value="STOPPED", text_color="red")
        window["-START-"].update(text="Start Server")

        stop_server()

        status = Status.STOPPED

    #Get the password
    elif event == "-PASSWORD-":

        password = values["-PASSWORD-"]

    #Get the port
    elif event == "-PORT-":

        port = values["-PORT-"]


window.close()