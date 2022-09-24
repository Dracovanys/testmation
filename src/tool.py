import os
from commands import *

root = os.getcwd()

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

    elif command.find("OPEN") > -1:
        app = command[command.find("(") + 1:command.find(")")].strip()
        os.system(openApp(app))

def getCommands(test_case:str):
    if not os.path.exists(f"{root}/test-cases"):
        os.mkdir(f"{root}/test-cases")
        print(f"'{test_case}' not found. Please create it on 'test-cases' folder.")
        return
    else:
        if not os.path.exists(f"{root}/test-cases/{test_case}.tca"):
            print(f"'{test_case}' not found. Please create it on 'test-cases' folder.")
            return
        else:
            with open(f"{root}/test-cases/{test_case}.tca", "r") as test_caseCommads:
                commands = test_caseCommads.readlines()
                return commands

