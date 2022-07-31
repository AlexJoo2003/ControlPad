
# Control Pad

A Control Pad is a tool which you can use to play sounds or execute hot keys. By connecting a Launchpad (currently only Launchpad Mini is supported) you can assign buttons different functions.


## Features

- No GUI
- Assign and delete buttons
- Raise and Lower Volume, Stop Sound
- Sound buttons to play sounds and music
- HotKey buttons to execute hotkeys with a single press


## Installation

#### On Windows:
1. Download manualy: Click on `ControlPad.exe` then click download and select destination
2. Download with curl: 
```
mkdir ControlPad
cd ControlPad
curl -o ControlPad.exe https://github.com/AlexJoo2003/ControlPad/raw/master/ControlPad.exe
```
## Usage
In order to succesfully use the application, you need to have a Launchpad connected to the PC. The application has only been tested on a Launchpad Mini by Novation. Once connected, run the `ControlPad.exe`.
If all is done correctly the launchpad should have 1 PageButton lit up at the top, and a couple other MetaButtons on the right side.

#### Different Buttons
Top row is for the `PageButtons`, they dictate which page is currently selected for the grid
The right column shows the `MetaButtons`, they have special functions which stay the same on every page.
The big area in the middle is the Grid, which is filled by different `FunctionButtons` such as `SoundButtons` and `HotKeyButtons`
#### MetaButton functions
Here are the functions of the `MetaButtons` top to bottom (in the default configuration):
1. Raise Volume - raised the volume of the application by 10%
2. Lower Volume - same as above but the other way around
3. Stop Sound - Stops any sound the application is running
4. Empty
5. Create a button - This enables you to create new buttons (More on that down bellow)
6. Delete a button - same as above but the other way around
7. Empty
8. Exit - Cleanly exits the application (This is the preffered way of exiting)
#### Creating new buttons
When pressing the `Create Button` you will enable `create_mode`. This is established when the button changes color from `orange` to `green`.

In order to create a `SoundButton`, you need to have an `.mp3` file downloaded on the system.
In the explorer click on the file and then click on the `copy path` button.
You can now press on any button in the grid to assign that sound file to it.
If everything was done correctly, the `Create Button` would turn back to `orange` and the new grid button would lit up `green`

In order to create a `HotKeyButton`, write down a sequence of keys separeted by spaces and copy it.
Then simply press on any available grid button, you should have a new button lit up `orange`.

NOTE: You can copy the `path to the file` or the `key sequence` even before you have enabled `create_mode`. As long as the value in the clipboard is a correct, this will work.

NOTE: You wont be able to create a new button where a button already exists, the `create_mode` will simply turn off.

NOTE: [Here](https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys) can you find accepted keys to use in the sequence with exception of space

#### Deleting buttons
The idea of deleting buttons is similar to creating new buttons but even simplier. Just press the `Delete Button` and `delete_mode` will enable whilst turning the button from `orange` to `red`.
Press on any existing button in the grid and it will dissapear and turn off the `delete_mode`.

NOTE: You wont be able to delete any non-grid buttons, i.e. `PageButtons` and `MetaButtons`

#### Extra
Please refrain from unpluging the launchpad before you have exited the application using the `ExitButton`. If it does happen anyway, in the system tray you can click on the green circle and press exit.
While that option is always available it is not recomended because it will not be able to clear the Launchpad buffer and some bugs may occur on the next launch.

## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

