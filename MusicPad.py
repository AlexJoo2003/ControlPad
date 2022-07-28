from pygame import mixer    # To play sounds
from os.path import exists  # To check if the config file exists
import json # To read and write the config file
from time import sleep
from pprint import pprint

#TODO: Detect launchpad button presses
#TODO: Manipulate launchpad button lights
#TODO: Play/Stop a sound and rise/lower the volume
#TODO: Assing commands to buttons
#TODO: Download mp3s
#TODO: Read and Write settings to a json file.

pad = None  # Global MusicPad object
lp = None   # Global Launchpad object

class Button:
    def __init__(self, position, **args):
        self.position = position
        self.args = args
        self.color = "white"
    
    def run(self):
        print("Button pressed")
    
    def changeColor(self, color):   
        self.color = color
        # lp.position color etc etc...

class PageButton(Button):
    def __init__(self, position, **args):
        Button.__init__(self, position, **args)
        self.page = position[0]
        self.selected = False
    
    def run(self):
        pad.changePage(self.page)
        print("Changed page to ", self.page)

class MetaButton(Button):
    def __init__(self, position, **args):
        Button.__init__(self, position, **args)

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
        self.in_action = False

    def run(self):
        if self.in_action:
            if mixer.music.get_busy():
                mixer.music.pause()
            else:
                mixer.music.unpause()
        else:
            for button in pad.buttons:  # This loop makes this button the only button in action
                if isinstance(button, SoundButton):
                    if button != self:
                        button.in_action = False
            self.in_action = True
            mixer.music.load(self.path)
            mixer.music.play()
            print("Playing Sound")
    
class MusicPad:
    def __init__(self):

        self.config_path = "./config.json"
        config = self.loadConfig()

        self.buttons = []
        for button in config["buttons"]:
            constructor = globals()[button["class"]]    # Finds the class from a string...
            instance = constructor(button["position"], **button["args"])  # then creates the object
            self.buttons.append(instance)
        
        self.current_page = config["current_page"]

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
                    return button
                buttons.append(button)
        for button in buttons:
            if button.page == args["page"]:
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
            self.buttons.remove(button)
            self.saveConfig()
            print("Deleted a button")
        else:
            print("Cannot delete a non-existing button")

    def pressButton(self, position):
        if button := self.searchButton(position, page = self.current_page):
            print("Pressing the button")
            button.run()
        else:
            print("Couldn't press the button, the button doesn't exist")
            # Create a new button perhaps
    
    def changePage(self, page):
        if page != self.current_page:
            self.current_page = page
            for button in self.buttons:
                if isinstance(button, PageButton):
                    if button.page != page:
                        button.changeColor("white")
                    else:
                        button.changeColor("green")

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

def main():
    mixer.init()                
    
    global pad
    pad = MusicPad()

    


if __name__ == "__main__":
    main()