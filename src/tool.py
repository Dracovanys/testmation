import os
from touch import *

def sendCommand(command:str):

    if command.find("TAP") > -1:
        x = command[command.find("(") + 1:command.find(",")].strip()
        y = command[command.find(",") + 1:command.find(")")].strip()
        os.system(tap(x, y))

    elif command.find("SWIPE") > -1:
        x1 = command[command.find("(") + 1:command.find(",")].strip()
        y1 = command[command.find(x1) + (len(x1) + 1):command.find(",", command.find(x1) + (len(x1) + 1))].strip()
        x2 = command[command.find(y1) + (len(y1) + 1):command.find(",", command.find(y1) + (len(y1) + 1))].strip()

        # Conditional logic in case of user don't give duration
        if command.find(",", command.find(x2) + (len(x2) + 1)) > -1:
            y2 = command[command.find(x2) + (len(x2) + 1):command.find(",", command.find(x2) + (len(x2) + 1))].strip()
            duration = command[command.find(y2) + (len(y2) + 1):command.find(")", command.find(y2) + (len(y2) + 1))].strip()
            os.system(swipe(x1, y1, x2, y2, duration))
        elif command.find(")", command.find(x2) + (len(x2) + 1)) > -1:
            y2 = command[command.find(x2) + (len(x2) + 1):command.find(")", command.find(x2) + (len(x2) + 1))].strip()
            os.system(swipe(x1, y1, x2, y2))

    elif command.find("DRAGDROP") > -1:
        x1 = command[command.find("(") + 1:command.find(",")].strip()
        y1 = command[command.find(x1) + (len(x1) + 1):command.find(",", command.find(x1) + (len(x1) + 1))].strip()
        x2 = command[command.find(y1) + (len(y1) + 1):command.find(",", command.find(y1) + (len(y1) + 1))].strip()
        y2 = command[command.find(x2) + (len(x2) + 1):command.find(",", command.find(x2) + (len(x2) + 1))].strip()
        duration = command[command.find(y2) + (len(y2) + 1):command.find(")", command.find(y2) + (len(y2) + 1))].strip()
        os.system(dragAndDrop(x1, y1, x2, y2, duration))



sendCommand("TAP(23, 59)")
sendCommand("SWIPE(123.5, 694.8, 213.4, 2321.2, 5000)")
sendCommand("DRAGDROP(123.5, 694.8, 213.4, 2321.2, 5000)")

