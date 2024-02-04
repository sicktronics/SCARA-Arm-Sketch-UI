# hello_world.py
## this is just an initial test!

import PySimpleGUI as sg

# Create a window
# sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()

sg.theme('DarkAmber')   # Add a touch of color

subs_size = 3
im_dim = 80

# All the stuff inside your window.
layout = [  [sg.Frame(title='Shape Selection', layout=[
                [sg.Button('SQUARE', image_source="square.PNG", image_subsample=subs_size, image_size=(im_dim, im_dim)), 
                 sg.Button('TRIAGNLE', image_source="triangle.PNG", image_subsample=subs_size, image_size=(im_dim, im_dim)), 
                 sg.Button('CIRCLE', image_source="circle.PNG", image_subsample=subs_size, image_size=(im_dim, im_dim)), 
                 sg.Button('HEXAGON', image_source="hexagon.PNG", image_subsample=subs_size, image_size=(im_dim, im_dim)), 
                 sg.Button('STAR', image_source="star.PNG", image_subsample=subs_size, image_size=(im_dim, im_dim)),]
            ])],
            [sg.Frame(title='Utensil Selection', layout=[
                [sg.Button('PEN\n[M06-T1]'), 
                 sg.Button('PENCIL\n[M06-T2]'), 
                 sg.Button('CRAYON\n[M06-T3]'),]
            ])],
            [sg.Frame(title='Manual GCode', layout=[
                [sg.Text('ENTER GCODE COMMAND:'), sg.InputText()]
            ])],
            [sg.Frame(title='GCode Command Guide', layout=[
                [sg.Text('''  Rapid Positioning: G00 X{x_coord} Y{y_coord}
                            \nLinear Interpolation: G01 X{x_coord} Y{y_coord} F{speed}
                            \nAbsolute Positioning: G90
                            \nRelative Positioning: G91
                            \nSet Units to Inches: G20
                            \nSet Units to Millimeters: G21
                            \nEnd the Program: M02
                            \nChange Writing Utensil: M06-{tool_#}
                            \nSave Current State: M70
                            \nRestore Saved State: M72''')]
            ])],
        ]

# Create the Window
window = sg.Window('SCARA Robotic Arm Interface', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', event)

window.close()