import launchpad_py as launchpad        # launchpad library which will detect imputs and manipulate lights on the launchpad
import json                             # Needed to save the commands and settings to an external json file stored in #! PATH_TO_SETTINGS.JSON


if launchpad.Launchpad().Check(0):
    lp = launchpad.Launchpad()
    if lp.Open(0):
        print("Launchpad Mk1/S/Mini")
else:
    print("Launchpad not available")
    exit()




#TODO: Detect launchpad button presses
#TODO: Manipulate launchpad button lights
#TODO: Play/Stop a sound and rise/lower the volume
#TODO: Assing commands to buttons
#TODO: Download mp3s
