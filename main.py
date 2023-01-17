import PySimpleGUI as sg

layout = [[sg.Text('Enter your password')],
          [sg.Input(password_char='*')],
          [sg.Button('Submit')]]

window = sg.Window('Password Input').Layout(layout)

while True:
    event, values = window.Read()
    if event is None or event == 'Submit':
        break
password = values[0]
print(password)
window.Close()