#!/usr/bin/python3

import PySimpleGUI as sg
import os
import subprocess
import sys
from enum import Enum

import asyncio ###
import asyncvnc.asyncvnc as asyncvnc
from PIL import Image
class Status(Enum):

    RUNNING = 1

    STOPPED = 2

def stop_client():
    try:
        if status == Status.RUNNING:
            client.terminate()
    except:
        pass

# imgName='screenshot.png'

# async def run_client():
#     async with asyncvnc.connect(addr,username=None,port=int(port),password=password) as client:
#         #print(client)
#         #client.keyboard.press('Super')
#         globalClient = client
#         screenshot = [
#             [sg.Image(key="-SCREENSHOT-")]
#         ]

#         clientWindow=sg.Window("Client: "+addr, [screenshot], size=(500, 300), finalize=True)

#         refreshRunning=False

#         while True:
#             # if disconnect == True:
#             #     disconnect = False
#             #     break

#             clientEvent, clientValues = clientWindow.read()
#             print('Stilll updating :)')

#             if refreshRunning == False:
#                 refreshRunning=True


#             if clientEvent == sg.WIN_CLOSED:
#                 break

#             if clientEvent == "-REFRESH-":
#                 refreshRunning=False
#                 if os.path.exists(imgName):
#                     clientWindow["-SCREENSHOT-"].update(filename=imgName)
#                     clientWindow.refresh()
#                     print('Screenshot updated')
#                     asyncio.sleep(1)
#                     os.remove(imgName)

#         clientWindow.close()
#         globalClient=None


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

        sg.In(size=(25, 1), enable_events=True, key="-PASSWORD-", password_char='*'),

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
        stop_client()
        break

    # Actual interface logic

    elif event == "-CONNECT-":
        stop_client() # in case the server is restarted with the same button
        try:
            # si = subprocess.STARTUPINFO()
            # si.dwFlags = subprocess.CREATE_NO_WINDOW
            client = subprocess.Popen([sys.executable, 'clientwindow.py', addr, port, password])#, startupinfo=si)
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