#!/usr/bin/python3

import PySimpleGUI as sg
import os

import asyncio
import asyncvnc.asyncvnc as asyncvnc

async def run_client():
    async with asyncvnc.connect(addr,username=None,port=int(port),password=password) as client:
        #print(client)
        client.keyboard.press('Super')

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
        sg.Text("Server Adress", expand_x=True),

        sg.In(size=(25, 1), enable_events=True, key="-ADDR-"),

    ],
    [
        sg.Text("Port", expand_x=True),

        sg.In(size=(25, 1), enable_events=True, key="-PORT-"),

    ],

    [
        sg.Text("Password", expand_x=True),

        sg.In(size=(25, 1), enable_events=True, key="-PASSWORD-"),

    ],

    [
        sg.Button(button_text="Connect", button_color="#275DA4", size=10, key="-CONNECT-"),

        sg.Button(button_text="Disconnect", button_color="red", size=10, key="-DISCONNECT-")
    ],

    # [
    #     sg.Text("Status: "),

    #     sg.Text("STOPPED", expand_y=True, text_color="red", key="-STATUS-")
    # ],

    [
        sg.Text(" ", expand_x=True),
        sg.Button(button_text="Quit", button_color="#808080", key="-QUIT-")
    ]
]


# Show the logo

image_viewer_column = [

    [sg.Image(key="-IMAGE-", filename=logo)]

]


# ----- Full layout -----

layout = [

    [

        sg.Column(image_viewer_column),

        sg.VSeperator(),

        sg.Column(parameter_list_column)
    ]

]


window = sg.Window("SimpleVNC Client", layout) #, icon='icon_square.ico')


# Run the Event Loop

while True:

    event, values = window.read()

    if event == "-QUIT-" or event == sg.WIN_CLOSED:
        
        break

    # Actual interface logic

    if event == "-CONNECT-":
        #window["-STATUS-"].update(value="RUNNING", text_color="#5DF455")
        asyncio.run(run_client())

    elif event == "-DISCONNECT-":
        #window["-STATUS-"].update(value="STOPPED", text_color="red")
        pass

    elif event == "-PASSWORD-":

        password = values["-PASSWORD-"]

    elif event == "-PORT-":

        port = values["-PORT-"]
    
    elif event == "-ADDR-":

        addr = values["-ADDR-"]


window.close()