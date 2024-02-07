'''
Author: Parker Mayer
Date: 02/06/2024
Junior Design II

Description: This python script genrates a GUI that processes
user input for our team's SCARA robotic arm. A user can enter 
the following input:

* GCODE movement commands (G00 or G01) manually. These get
  written to the GCODE.txt file for further processing by a 
  separate script.

* GCODE commands M-code commands that alter the status of the
  program (e.g., G21 to set units to mm or M02 to terminate).
  These get written to the STATUS.txt file for further processing 
  by a separate script.

* One of five shapes that the user wants the robotic arm to copy
  (written to the DRAWING.txt file for further processing 
  by a separate script).

* M06 or untensil selection that will inform the arm to swap in
  the specified utencil (pen, pencil, or crayon). The selection
  is written to the UTENSIL.txt file for further processing 
  by a separate script.

'''

# Importing relevant libraries
import PySimpleGUI as sg
import os

# Setting the GUI theme
sg.theme('DarkAmber')

# Global variables that impact displayed images
subs_size = 3
im_dim = 80

# The layout defines what is displayed in the window
layout = [  
            # This frame is responsible for selection of "shape" for the arm to draw
            [sg.Frame(title='Shape Selection', layout=[ 
                [sg.Button('SQUARE', image_source="../square.PNG", image_subsample=subs_size, image_size=(im_dim, im_dim)), 
                 sg.Button('TRIANGLE', image_source="../triangle.PNG", image_subsample=subs_size, image_size=(im_dim, im_dim)), 
                 sg.Button('CIRCLE', image_source="../circle.PNG", image_subsample=subs_size, image_size=(im_dim, im_dim)), 
                 sg.Button('HEXAGON', image_source="../hexagon.PNG", image_subsample=subs_size, image_size=(im_dim, im_dim)), 
                 sg.Button('STAR', image_source="../star.PNG", image_subsample=subs_size, image_size=(im_dim, im_dim)),]
            ])],
            # This frame is responsible for utensil selection (equivalent internally to using the "M06" command)
            [sg.Frame(title='Utensil Selection', layout=[
                [sg.Button('PEN'), 
                 sg.Button('PENCIL'), 
                 sg.Button('CRAYON'),]
            ])],
            # This frame is responsible for the user input of GCODE commands
            [sg.Frame(title='Manual GCode', layout=[
                [sg.Text('ENTER GCODE COMMAND:'), sg.InputText(do_not_clear=False), sg.Button('OK')]
            ])],
            # This frame provides a reference of available commands
            [sg.Frame(title='GCode Command Guide', layout=[
                [sg.Text('''Rapid Positioning: G00 X{x_coord} Y{y_coord}
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
    if event == sg.WIN_CLOSED: # If user closes window
        # Clearing the contents of each file....
        gcode_command_file = open('SCARA-Arm-Sketch-UI/GCODE.txt', 'w')
        utensil_file = open('SCARA-Arm-Sketch-UI/UTENSIL.txt', 'w')
        drawing_file = open('SCARA-Arm-Sketch-UI/DRAWING.txt', 'w')
        status_file = open('SCARA-Arm-Sketch-UI/STATUS.txt', 'w')
        gcode_command_file.close()
        utensil_file.close()
        drawing_file.close()
        status_file.close()
        break
    
    # If an event occurred, rather than user text input...
    if(not values[0]):
        # Check if a drawing was selected
        if(event=="SQUARE" or event=="TRIANGLE" or event=="CIRCLE"or event=="HEXAGON" or event=="STAR"):
            # Write the drawing selection to a file
            drawing_file = open('SCARA-Arm-Sketch-UI/DRAWING.txt', 'a')
            event+='\n'
            drawing_file.write(event)
            drawing_file.close()
        # Otherwise if a utensil was selected
        else:
            # Write the appropriate "M06" command to the status file
            command=''
            utensil_file = open('SCARA-Arm-Sketch-UI/UTENSIL.txt', 'a')
            if(event=="PEN"):
                utensil_file.write("M06-T1\n")
            if(event=="PENCIL"):
                utensil_file.write("M06-T2\n")
            if(event=="CRAYON"):
                utensil_file.write("M06-T3\n")
            utensil_file.close()

    # If not an event, then retrieve user text input
    else:
        # Try to gather the first three characters of
        # the command and throw an exception if
        # encounters and IndexError.
        command_type = ""
        try:
            for i in range(3):
                command_type+=values[0][i]
        except IndexError:
            sg.popup_no_buttons('Warning: Not a recognized command. Please try again.')
            continue
        # Notify user if an invalid command was provided
        if(command_type[0] != "G" and command_type[0] != "M"):
            sg.popup_no_buttons('Warning: Not a recognized command. Please try again.')
        # If a movement command was received...
        if(command_type=="G00" or command_type=="G01"):
            # Open the GCode file and write values[0] (the full command)
            write_str = ''
            for letter in values[0]:
                write_str+=letter
            write_str+='\n'
            gcode_command_file = open('SCARA-Arm-Sketch-UI/GCODE.txt', 'a')
            gcode_command_file.write(write_str)
            gcode_command_file.close()

        # If the utensil-switch command was received...
        elif(command_type=="M06"):
            # Open the utensil file and write values[0] (the full command)
            write_str = ''
            for letter in values[0]:
                write_str+=letter
            write_str+='\n'
            utensil_file = open('SCARA-Arm-Sketch-UI/UTENSIL.txt', 'a')
            utensil_file.write(write_str)
            utensil_file.close()

        # If the program termination command was received...
        elif(command_type=="M02"):
            # Time to shut it down!
            # Clearing the contents of each file....
            gcode_command_file = open('SCARA-Arm-Sketch-UI/GCODE.txt', 'w')
            utensil_file = open('SCARA-Arm-Sketch-UI/UTENSIL.txt', 'w')
            drawing_file = open('SCARA-Arm-Sketch-UI/DRAWING.txt', 'w')
            status_file = open('SCARA-Arm-Sketch-UI/STATUS.txt', 'w')
            gcode_command_file.close()
            utensil_file.close()
            drawing_file.close()
            status_file.close()
            break
        # Otherwise, update status (e.g., G20, G21, M70, etc)
        else:
            # Open the status file and write values[0] (the full command)
            write_str = ''
            for letter in values[0]:
                write_str+=letter
            write_str+='\n'
            status_file = open('SCARA-Arm-Sketch-UI/STATUS.txt', 'a')
            status_file.write(write_str)
            status_file.close()
        
window.close()