from pygame import mixer    # To play sounds
from os.path import exists  # To check if the config file exists
import json # To read and write the config file
from time import sleep
from pprint import pprint
import pyperclip
import os
import pyautogui
try:
    import launchpad_py as launchpad
except ImportError:
    try:
        import launchpad
    except ImportError:
        sys.exit("error loading launchpad.py")

#TODO: Detect launchpad button presses
#TODO: Manipulate launchpad button lights
#TODO: Play/Stop a sound and rise/lower the volume
#TODO: Assing commands to buttons
#TODO: Download mp3s
#TODO: Read and Write settings to a json file.

pad = None  # Global MusicPad object
lp = None   # Global Launchpad object
if launchpad.Launchpad().Check(0):
    lp = launchpad.Launchpad()
    if lp.Open(0):
        print("Launchpad Mk1/S/Mini")
    lp.Reset()
else:
    print("Launchpad not available")
    exit()

class Button:
    def __init__(self, position, **args):
        self.position = position
        self.args = args
        self.color = "white"
        self.changeColor(self.color)

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
        
        # lp.position color etc etc...

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
        self.changeColor(self.color)
    
    def run(self):
        self.function()
    
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
        exit()

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
        self.changeColor(self.color)

    def run(self):
        mixer.music.load(self.path)
        mixer.music.play()
        print("Playing Sound")

class HotKeyButton(FunctionButton):
    def __init__(self, position, **args):
        FunctionButton.__init__(self, position, **args)
        self.keys = args["keys"]
        self.color = "orange"
        self.changeColor(self.color)

    def run(self):
        for key in self.keys:           # Press down the Keys
            pyautogui.keyDown(key)
        for key in self.keys:           # Release the Keys
            pyautogui.keyUp(key)


class MusicPad:
    def __init__(self):
        self.config_path = "./config.json"
        config = self.loadConfig()
        self.current_page = config["current_page"]

        self.buttons = []
        
        self.create_mode = False
        self.delete_mode = False

    def createButtons(self):
        config = self.loadConfig()
        for button in config["buttons"]:
            constructor = globals()[button["class"]]    # Finds the class from a string...
            instance = constructor(button["position"], **button["args"])  # then creates the object
            self.buttons.append(instance)

    def loadConfig(self):
        print("Loading Config...")
        if not exists(self.config_path):    # Creates a new config if it is missing
            print("Config doens't exist, creating a new one...")
            with open(self.config_path, 'w') as f:
                json.dump({"buttons":[],"current_page": 0}, f, indent=4) 
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

    def purgeConfig(self):
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
            #! Give a warning popup
        else:
            self.buttons.append(new_button)
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

    def pressButton(self, position):
        self.delete_mode = False
        self.create_mode = False
        for button in pad.buttons:      # This turns off the delete_mode and create_mode if they are turned on
            if isinstance(button, MetaButton) and hasattr(button, "function_name"):
                if "mode_toggle" in button.function_name and button.color != "orange":
                    button.changeColor("orange")

        if button := self.searchButton(position, page = self.current_page):
            if isinstance(button, FunctionButton) and self.delete_mode:
                self.deleteButton(position, page = self.current_page)
                for button in self.buttons:
                    if hasattr(button, "function_name"):
                        if button.function_name == "delete_mode_toggle":
                            button.run()            # Turns off the delete mode and turns the button back to orange
            else:
                print("Pressing the button")
                button.run()
        else:
            if self.create_mode:
                path = pyperclip.paste()
                if path.startswith('"') and path.endswith('"'):
                    path = path[1:-1]   # remove the double quotes if the user used the copy function in the explorer
                if os.path.exists(path):                             # Use the path for the song
                    pad.createButton(position, SoundButton, path = path, page = self.current_page)
                    for button in self.buttons:
                        if hasattr(button, "function_name"):
                            if button.function_name == "create_mode_toggle":
                                button.run()            # Turns off the create mode and turns the button back to orange
                else:
                    print("Path doesn't exist", path)
            else:
                print("Couldn't press the button, the button doesn't exist")

    def changePage(self, page):
        for button in self.buttons:     # Turns off all the buttons on the current page
            if isinstance(button, FunctionButton):
                if button.page == self.current_page:
                    button.changeColor("white")

        if page != self.current_page:
            for button in self.buttons:
                if isinstance(button, PageButton): # Turns the selected page green while every other page white
                    if button.page != page:
                        if button.color != "white":
                            button.changeColor("white") 
                    else:
                        button.changeColor("green")
                if isinstance(button, FunctionButton):  # Turns off all the buttons on the current page and turns on the buttons on the new page
                    if button.page == self.current_page:
                        button.changeColor("white")
                    elif button.page == page:
                        button.changeColor("green")
            self.current_page = page

def pause_test():
    pad.purgeConfig()
    pad.createButton([0,0], SoundButton, page = 0, path = "C:/Users/alexa/Music/memes/CurbYour.mp3")
    pad.createButton([0,1], SoundButton, page = 0, path = "C:/Users/alexa/Music/memes/TheOnlyThingTheyFearIsYou.mp3")
    print(">>> play curb")
    input()
    pad.pressButton([0,0])
    print(">>> pause curb")
    input()
    pad.pressButton([0,0])
    print(">>> play doom")
    input()
    pad.pressButton([0,1])
    print(">>> play curb")
    input()
    pad.pressButton([0,0])
    print(">>> pause curb")
    input()
    pad.pressButton([0,0])
    print(">>> unpause curb")
    input()
    pad.pressButton([0,0])
    input(">>> done")

def create_delete_test():
    pad.purgeConfig()
    input(">>> Create a SoundButton...")
    pad.createButton([0,0], SoundButton, page = 0, path = "C:/Users/alexa/Music/memes/CurbYour.mp3")
    input(">>> Delete that SoundButton...")
    pad.deleteButton([0,0], page = 0)
    print("==================================")
    input(">>> Create a PageButton...")
    pad.createButton([0,0], PageButton)
    input(">>> Delete that PageButton...")
    pad.deleteButton([0,0])
    input(">>> Done")

def page_test():
    pad.purgeConfig()
    input(">>> Create two SoundButtons and two Page buttons, current_page is 0")
    pad.createButton([0,0], PageButton)
    pad.createButton([1,0], PageButton)
    pad.createButton([0,1], SoundButton, page = 0, path = "C:/Users/alexa/Music/memes/CurbYour.mp3")
    pad.createButton([1,1], SoundButton, page = 1, path = "C:/Users/alexa/Music/memes/TheOnlyThingTheyFearIsYou.mp3")
    pad.changePage(0)
    input(">>> Press 0,0, should work cause the button is on page 0")
    pad.pressButton([0,1])
    input(">>> Press 1,1, should NOT work cause the button is on page 1")
    pad.pressButton([1,1])
    input(">>> Change the page to 1")
    pad.pressButton([1,0])
    input(">>> Press 0,1, should NOT work cause the button is on page 0")
    pad.pressButton([0,1])
    input(">>> Press 0,1, should work cause the button is on page 1")
    pad.pressButton([1,1])
    input(">>> Done")
    pad.purgeConfig()

def LaunchPadMk1_default_setup():

    pad.deleteButton([0,0])
    pad.deleteButton([1,0])
    pad.deleteButton([2,0])
    pad.deleteButton([3,0])
    pad.deleteButton([4,0])
    pad.deleteButton([5,0])
    pad.deleteButton([6,0])
    pad.deleteButton([7,0])
    pad.deleteButton([8,1])
    pad.deleteButton([8,2])
    pad.deleteButton([8,3])
    pad.deleteButton([8,5])
    pad.deleteButton([8,6])
    pad.deleteButton([8,8])

    pad.createButton([0,0], PageButton)
    pad.createButton([1,0], PageButton)
    pad.createButton([2,0], PageButton)
    pad.createButton([3,0], PageButton)
    pad.createButton([4,0], PageButton)
    pad.createButton([5,0], PageButton)
    pad.createButton([6,0], PageButton)
    pad.createButton([7,0], PageButton)
    pad.createButton([8,1], MetaButton, function = "raise_volume")
    pad.createButton([8,2], MetaButton, function = "lower_volume")
    pad.createButton([8,3], MetaButton, function = "stop_music")
    pad.createButton([8,5], MetaButton, function = "create_mode_toggle")
    pad.createButton([8,6], MetaButton, function = "delete_mode_toggle")
    pad.createButton([8,8], MetaButton, function = "exit")

def main():

    mixer.init()                
    
    global pad
    pad = MusicPad()
    pad.createButtons()

    # LaunchPadMk1_default_setup()
    
    while True:
        buts = lp.ButtonStateXY()
        if buts:
            if not buts[-1]:
                position = [buts[0], buts[1]]
                pad.pressButton(position)


if __name__ == "__main__":
    main()