from pygame import mixer    # To play sounds
from os.path import exists  # To check if the config file exists
import json # To read and write the config file
import pyperclip # To get the clipboard value
import os.path # To check if a sound file path exists on the system
import pyautogui # To emulate keyboard presses
import sys  # To exit without error
try:
    import launchpad_py as launchpad # To connect to a launchpad (So far suppots only the Mini version)
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("error loading launchpad.py")

pad = None  # Global MusicPad object
lp = None   # Global Launchpad object
if launchpad.Launchpad().Check(0):
    lp = launchpad.Launchpad()
    if lp.Open(0):
        print("Launchpad Mk1/S/Mini")
    lp.Reset()
else:
    print("Launchpad not available")
    sys.exit()

class Button:
    def __init__(self, position, **args):
        self.position = position
        self.args = args

    def run(self):
        print("Button pressed")
    
    def changeColor(self, color):
        self.color = color
        if color == "green":
            lp.LedCtrlXY(self.position[0], self.position[1], 0, 1)
        elif color == "orange":
            lp.LedCtrlXY(self.position[0], self.position[1], 1, 1)
        elif color == "red":
            lp.LedCtrlXY(self.position[0], self.position[1], 1, 0)
        elif color == "white":
            lp.LedCtrlXY(self.position[0], self.position[1], 0, 0)
        print("Changed", self.position, " color to ", self.color)
        
class PageButton(Button):
    def __init__(self, position, **args):
        Button.__init__(self, position, **args)
        self.page = position[0]
        self.selected = False
        if pad.current_page == self.page:
            self.color = "green"
        else:
            self.color = "white"
        self.changeColor(self.color)
    
    def run(self):
        pad.changePage(self.page)
        print("Changed page to ", self.page)

class MetaButton(Button):
    def __init__(self, position, **args):
        Button.__init__(self, position, **args)
        self.function_name = args["function"]
        self.function = getattr(self, self.function_name)
        self.color = "green"
        if self.function_name == "exit":
            self.color = "red"
        elif "mode_toggle" in self.function_name:
            self.color = "orange"
        elif self.function_name == "empty_function":
            self.color = "white"
        self.changeColor(self.color)
    
    def run(self):
        self.function()
    
    def empty_function(self):
        print("This is a placeholder MetaButton")           # This is used just so the user can\t add a functionbutton to where a metaButton is supposed to be

    def change_volume(self, volume):
        current_volume = mixer.music.get_volume()
        new_volume = current_volume + volume
        
        if new_volume <= 0:
            new_volume = 0
        elif new_volume >= 1:
            new_volume = 1
        
        print("changed volume to ", new_volume)
        mixer.music.set_volume(new_volume)
    
    def lower_volume(self):
        self.change_volume(-0.1)
    
    def raise_volume(self):
        self.change_volume(0.1)
    
    def stop_music(self):
        mixer.music.stop()
        print("stopped the music")
    
    def toggle_pause_music(self):
        if mixer.music.get_busy():
            mixer.music.pause()
        else:
            mixer.music.unpause()

    def create_mode_toggle(self):
        if pad.create_mode:
            self.changeColor("orange")
        else:
            self.changeColor("green")
            
        pad.create_mode = not pad.create_mode

    def delete_mode_toggle(self):
        if pad.delete_mode:
            self.changeColor("orange")
        else:
            self.changeColor("red")

        pad.delete_mode = not pad.delete_mode

    def exit(self):
        print("exiting")
        mixer.music.stop()
        lp.Reset()
        lp.Close()
        sys.exit()

class FunctionButton(Button):
    def __init__(self, position, **args):
        Button.__init__(self, position, **args)
        self.page = args["page"]
    
    def run():
        print("Running a Function Button")

class SoundButton(FunctionButton):
    def __init__(self, position, **args):
        FunctionButton.__init__(self, position, **args)
        self.path = args["path"]
        self.color = "green"

    def run(self):
        mixer.music.load(self.path)
        mixer.music.play()
        print("Playing Sound")

class HotKeyButton(FunctionButton):
    def __init__(self, position, **args):
        FunctionButton.__init__(self, position, **args)
        self.keys = args["keys"]
        self.color = "orange"

    def run(self):
        for key in self.keys:           # Press down the Keys
            pyautogui.keyDown(key)
        for key in self.keys:           # Release the Keys
            pyautogui.keyUp(key)
        print("Keybind pressed")


class MusicPad:
    def __init__(self, model = "Mini"):
        self.config_path = "./config.json"
        self.buttons = []
        self.create_mode = False
        self.delete_mode = False
        self.model = model
        config = self.loadConfig()
        self.current_page = config["current_page"]

    def createButtons(self):
        config = self.loadConfig()
        if not config["buttons"]:
            self.defaultSetup()
        for button in config["buttons"]:
            constructor = globals()[button["class"]]    # Finds the class from a string...
            instance = constructor(button["position"], **button["args"])  # then creates the object
            if isinstance(instance, FunctionButton):    # Only show the buttons on the current page
                if instance.page == self.current_page:
                    instance.changeColor(instance.color)
            self.buttons.append(instance)

    def loadConfig(self):
        print("Loading Config...")
        if not exists(self.config_path):    # Creates a new config if it is missing
            print("Config doens't exist, creating a new one...")
            self.resetConfig()
        config = {}
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        print("Loaded the config")
        return config

    def saveConfig(self):
        config = self.loadConfig()
        print("Saving Config...")
        config["buttons"] = []
        for button in self.buttons:
            config["buttons"].append({
                "class": type(button).__name__, # Gets the name of the class from the object
                "position": button.position,
                "args": button.args
            })
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print("Config saved")

    def resetConfig(self):
        print("Purging Config...")
        with open(self.config_path, 'w') as f:
            json.dump({"buttons": [], "current_page": 0}, f, indent=4)
        print("Config cleared")

    def searchButton(self, position, **args):
        buttons = []
        for button in self.buttons:
            if button.position == position:
                if not isinstance(button, FunctionButton):         # return any non grid based button in the same position
                    print("Found a non grid button at ", position)
                    return button
                buttons.append(button)
        for button in buttons:
            if button.page == args["page"]:
                print("Found a grid button at ", position)
                return button                           # return the grid based button on the same page

    def createButton(self, position, button_class, **args):
        new_button = button_class(position, **args)
        if self.searchButton(position, **args):
            print("This button is occupied")
        else:
            self.buttons.append(new_button)
            if isinstance(new_button, FunctionButton):
                if new_button.page == self.current_page:
                    new_button.changeColor(new_button.color)
            self.saveConfig()
            print("Created a new button")

    def deleteButton(self, position, **args):
        if button := self.searchButton(position, **args):
            button.changeColor("white")
            self.buttons.remove(button)
            self.saveConfig()
            print("Deleted a button")
        else:
            print("Cannot delete a non-existing button")

    def turn_off_mode(self, mode):
        print("turning off ", mode)
        if mode == "create_mode_toggle":
            for button in self.buttons:
                if hasattr(button, "function_name"):
                    if button.function_name == "create_mode_toggle":    # Turns off the create mode and turns the button back to orange
                        button.changeColor("orange")
                        self.create_mode = False
        elif mode == "delete_mode_toggle":
            for button in self.buttons:
                if hasattr(button, "function_name"):
                    if button.function_name == "delete_mode_toggle":    # Turns off the delete mode and turns the button back to orange
                        button.changeColor("orange")
                        self.delete_mode = False

    def pressButton(self, position):

        if button := self.searchButton(position, page = self.current_page):     # If the button exists
            if self.create_mode:
                self.turn_off_mode("create_mode_toggle")
            else:
                if self.delete_mode:                                            # if in delete mode
                    if isinstance(button, FunctionButton):
                        self.deleteButton(position, page = self.current_page)   # Only delete FunctionButton
                    self.turn_off_mode("delete_mode_toggle")
                else:
                    print("Pressing the button")
                    button.run()
        else:                                   # if the button doesn\t exist
            if self.create_mode:                # create a button if in create mode
                self.turn_off_mode("create_mode_toggle")
                command = pyperclip.paste()
                if command.startswith('"') and command.endswith('"'):
                    command = command[1:-1]   # remove the double quotes if the user used the copy function in the file explorer
                if os.path.exists(command) and command.endswith(".mp3"):                             # If it is a path and is an mp3 file, create a SoundButton
                    pad.createButton(position, SoundButton, path = command, page = self.current_page)
                else:
                    commands =  " ".join(command.split()).split(" ")   # this removes whitespaces and makes a list of keys
                    is_valid = True
                    for command in commands:
                        if not command in pyautogui.KEYBOARD_KEYS:
                            print("Command unkown")
                            is_valid = False
                            break
                    if is_valid:
                        self.createButton(position, HotKeyButton, keys = commands, page = self.current_page)
                    
            else:
                if self.delete_mode:
                    self.turn_off_mode("delete_mode_toggle")
                print("Couldn't press the button, the button doesn't exist")
        
    def changePage(self, page):
        if page != self.current_page:
            for button in self.buttons:
                print(type(button))
                if isinstance(button, PageButton): # Turns the selected page green while every other page white
                    if button.page != page:
                        if button.color != "white":
                            button.changeColor("white") 
                    else:
                        button.changeColor("green")
                elif isinstance(button, FunctionButton):  # Turns off all the buttons on the current page and turns on the buttons on the new page
                    if button.page == self.current_page:
                        # print("Turned off a button")
                        if not self.searchButton(button.position, page = page): # Only remove the color if there isn't another button to take it's place
                            button.changeColor("white")
                    elif button.page == page:
                        # print("Turned on a button")
                        if isinstance(button, SoundButton):
                            button.changeColor("green")
                        elif isinstance(button, HotKeyButton):
                            button.changeColor("orange")
            self.current_page = page

    def defaultSetup(self):          # This is my prefered setup for my Launchpad Mini, if you have a different model that launchpad.py supports then it's possible to create a setup for it too
        if self.model == "Mini":
            self.deleteButton([0,0])
            self.deleteButton([1,0])
            self.deleteButton([2,0])
            self.deleteButton([3,0])
            self.deleteButton([4,0])
            self.deleteButton([5,0])
            self.deleteButton([6,0])
            self.deleteButton([7,0])
            self.deleteButton([8,1])
            self.deleteButton([8,2])
            self.deleteButton([8,3])
            self.deleteButton([8,4])
            self.deleteButton([8,5])
            self.deleteButton([8,6])
            self.deleteButton([8,7])
            self.deleteButton([8,8])

            self.createButton([0,0], PageButton)
            self.createButton([1,0], PageButton)
            self.createButton([2,0], PageButton)
            self.createButton([3,0], PageButton)
            self.createButton([4,0], PageButton)
            self.createButton([5,0], PageButton)
            self.createButton([6,0], PageButton)
            self.createButton([7,0], PageButton)
            self.createButton([8,1], MetaButton, function = "raise_volume")
            self.createButton([8,2], MetaButton, function = "lower_volume")
            self.createButton([8,3], MetaButton, function = "stop_music")
            self.createButton([8,4], MetaButton, function = "empty_function")
            self.createButton([8,5], MetaButton, function = "create_mode_toggle")
            self.createButton([8,7], MetaButton, function = "empty_function")
            self.createButton([8,6], MetaButton, function = "delete_mode_toggle")
            self.createButton([8,8], MetaButton, function = "exit")

def main():

    mixer.init()                
    
    global pad
    pad = MusicPad()
    pad.createButtons()

    while True:             # Detects Launchpad Presses
        buts = lp.ButtonStateXY()
        if buts:
            if not buts[-1]:
                position = [buts[0], buts[1]]
                pad.pressButton(position)


if __name__ == "__main__":
    main()