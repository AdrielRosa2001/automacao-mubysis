import PySimpleGUI as sg

sg.theme('Reddit')

layout = [
    [sg.Text('Aguarde um momeno\nRealizando o seguinte procedimentos:')],
    [sg.Button('Aplicar')]
]

window = sg.Window('Modulo de automações - Muby', layout, icon='./assets/icon2.0.ico')

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Close':
        break