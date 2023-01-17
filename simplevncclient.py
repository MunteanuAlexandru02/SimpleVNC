#!/usr/bin/python3

import PySimpleGUI as sg
import os
import subprocess
import sys
from enum import Enum

import asyncio ###
import asyncvnc.asyncvnc as asyncvnc
from PIL import Image

#   Basically, the first page of the
#   client will do almost the same thing as the server
#   and that is to provide a simple GUI logging screen for the user.
#   The only main difference is the "Server Address" text box.
#   For a simple way to test the client and the server we recommend to
#   start the server on your own machine and introduce in the
#   "Server Address" zone: localhost, that should start the "SimpleVNC"
#   on your machine.

#client status
class Status(Enum):

    RUNNING = 1

    STOPPED = 2

def stop_client():
    try:
        if status == Status.RUNNING:
            client.terminate()
    except:
        pass

logo = os.path.abspath("simplevnc.png")

if not os.path.exists(logo):
    logo = ""

password=""
port=""
addr=""


# First the window layout in 2 columns

parameter_list_column = [

    [
        sg.Text("Server Parameters")
    ],

	[
        sg.Text("Server Adress", expand_x = True),

        sg.In(size = (25, 1), enable_events = True, key = "-ADDR-"),

    ],
    [
        sg.Text("Port", expand_x = True),

        sg.In(size = (25, 1), enable_events = True, key = "-PORT-"),

    ],

    [
        sg.Text("Password", expand_x = True),

        sg.In(size = (25, 1), enable_events = True, key = "-PASSWORD-", password_char = '*'),

    ],

    [
        sg.Button(button_text = "Connect", button_color = "#275DA4", size = 10, key = "-CONNECT-"),

        sg.Button(button_text = "Disconnect", button_color = "red", size = 10, key = "-DISCONNECT-")
    ],

    [
        sg.Text(" ", expand_x = True),
        sg.Button(button_text = "Quit", button_color = "#808080", key = "-QUIT-")
    ]
]


# Show the logo

image_viewer_column = [

    [sg.Image(key="-IMAGE-", filename = logo)]

]


# ----- Full layout -----

layout = [

    [

        sg.Column(image_viewer_column),

        sg.VSeperator(),

        sg.Column(parameter_list_column)
    ]

]


window = sg.Window("SimpleVNC Client", layout)

# Run the Event Loop

while True:

    event, values = window.read()

    if event == "-QUIT-" or event == sg.WIN_CLOSED:
        stop_client()
        break

    # Actual interface logic

    elif event == "-CONNECT-":

        stop_client() # in case the client is restarted with the same button

        try:
            client = subprocess.Popen([sys.executable, 'clientwindow.py', addr, port, password])
            status = Status.RUNNING

        except:
            pass

    elif event == "-DISCONNECT-":
        stop_client()
        status = Status.STOPPED

    elif event == "-PASSWORD-":
        password = values["-PASSWORD-"]

    elif event == "-PORT-":
        port = values["-PORT-"]
    
    elif event == "-ADDR-":
        addr = values["-ADDR-"]

window.close()