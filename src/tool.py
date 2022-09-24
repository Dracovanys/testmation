import sys
import os
import numpy as np
from sewar.full_ref import uqi
from PIL import Image
from time import sleep
from commands import *

root = os.getcwd()

def sendCommand(command:str, result:list, result_folder:str):

    '''
    Different treatment for each
    command.
    '''   

    sentCommand = "adb "

    if command.find("TAP") > -1:
        x = command[command.find("(") + 1:command.find(",")].strip()
        y = command[command.find(",") + 1:command.find(")")].strip()
        sentCommand += tap(x, y)
        result.append("Pass")

    elif command.find("SWIPE") > -1:

        x1_position = command.find("(") + 1
        x1 = command[x1_position:command.find(",", x1_position)].strip()
        y1_position = command.find(",", x1_position) + 1
        y1 = command[y1_position:command.find(",", y1_position)].strip()
        x2_position = command.find(",", y1_position) + 1
        x2 = command[x2_position:command.find(",", x2_position)].strip()        

        # Conditional logic in case of user don't give duration
        if command.find(",", x2_position + (len(x2) + 2)) > -1:
            y2_position = command.find(",", x2_position) + 1
            y2 = command[y2_position:command.find(",", y2_position)].strip()
            duration_position = command.find(",", y2_position) + 1
            duration = command[duration_position:command.find(")", duration_position)].strip()
            sentCommand += swipe(x1, y1, x2, y2, duration)
        elif command.find(")", x2_position + (len(x2) + 2)) > -1:
            y2_position = command.find(",", x2_position) + 1
            y2 = command[y2_position:command.find(",", y2_position)].strip()
            sentCommand += swipe(x1, y1, x2, y2)
        
        result.append("Pass")

    elif command.find("DRAGDROP") > -1:
        x1 = command[command.find("(") + 1:command.find(",")].strip()
        y1 = command[command.find(x1) + (len(x1) + 1):command.find(",", command.find(x1) + (len(x1) + 1))].strip()
        x2 = command[command.find(y1) + (len(y1) + 1):command.find(",", command.find(y1) + (len(y1) + 1))].strip()
        y2 = command[command.find(x2) + (len(x2) + 1):command.find(",", command.find(x2) + (len(x2) + 1))].strip()
        duration = command[command.find(y2) + (len(y2) + 1):command.find(")", command.find(y2) + (len(y2) + 1))].strip()
        sentCommand += dragAndDrop(x1, y1, x2, y2, duration)
        result.append("Pass")

    elif command.find("OPEN") > -1:
        app = command[command.find("(") + 1:command.find(")")].strip()
        sentCommand += openApp(app)
        result.append("Pass")

    elif command.find("COMPARE_IMAGE") > -1:
        if not os.path.exists(f"{root}/reference"):
            os.mkdir(f"{root}/reference")
            result.append("Error")
            return

        referenceImage = command[command.find("(") + 1:command.find(",")].strip()
        passRate = float(command[command.find(",") + 1:command.find(")")].strip())

        if not os.path.exists(f"{root}/reference/{referenceImage}"):
            result.append("Error")
            return

        sentCommand_ = sentCommand + captureImage()
        validationImage = sentCommand_[sentCommand_.find("/", sentCommand_.find("sdcard")) + 1:]

        os.system(sentCommand_)        

        sentCommand_ = sentCommand + getImage(validationImage, result_folder)

        os.system(sentCommand_)

        original = np.array(Image.open(f"{result_folder}/{validationImage}"))
        reference = np.array(Image.open(f"{root}/reference/{referenceImage}"))

        comparison = uqi(original, reference) * 100
        
        if comparison >= passRate:
            result.append("Pass")
        else:
            result.append("Fail")
        return

    # Set sleep between tests
    if command.find("{") > -1:
        sleepTime = int(command[command.find("{") + 1:command.find("}")].strip())
    else:
        sleepTime = 1

    # Repeat command
    if command.find("[") > -1:
        for count in range(int(command[command.find("[") + 1:command.find("]")].strip())):
            os.system(sentCommand)
            sleep(sleepTime)
    else:
        os.system(sentCommand)
        sleep(sleepTime)

def getCommands(test_case:str):

    '''
    Return all commands in a TCA file
    as a string list
    '''

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
                commands = []
                for command in test_caseCommads.readlines():
                    if command[0] != "#":
                        commands.append(command.strip("\n"))
                return commands

def getTestCases(test_cycle:str):

    '''
    Return all test cases described in a
    TCY file as a string list
    '''

    if not os.path.exists(f"{root}/test-cycle"):
        os.mkdir(f"{root}/test-cycle")
        print(f"'{test_cycle}' not found. Please create it on 'test-cycle' folder.")
        return
    else:
        if not os.path.exists(f"{root}/test-cycle/{test_cycle}.tcy"):
            print(f"'{test_cycle}' not found. Please create it on 'test-cycle' folder.")
            return
        else:
            with open(f"{root}/test-cycle/{test_cycle}.tcy", "r") as test_cycleCases:
                testCases = []
                for testCase in test_cycleCases.readlines():
                    testCases.append(testCase.strip("\n"))
                return testCases

def execTestCycle(test_cycle:str):

    # Create folder for storage results
    if not os.path.exists(f"{root}/test-execution"):
            os.mkdir(f"{root}/test-execution")
    
    # Create test cycle folder
    result_folder = f"{root}/test-execution/{test_cycle}_{datetime.now().day}{datetime.now().month}{datetime.now().year}{datetime.now().hour}{datetime.now().minute}{datetime.now().second}"
    os.mkdir(result_folder)    

    # Start execution
    testCycle_log = []
    testCase_number = 1
    for testCase in getTestCases(test_cycle):

        # Creating test case folder
        testCase_results = f"{result_folder}/{testCase_number}_{testCase}"
        os.mkdir(testCase_results)

        # Sending commands to device
        logging = f"[EXECUTING] {testCase}"
        results = []
        for command in getCommands(testCase):
            if command != "":                
                sendCommand(command, results, testCase_results)            
                logging += "."
                sys.stdout.write("\r")
                sys.stdout.write(logging)
                sys.stdout.flush()

        # Logging results
        if "Fail" in results:
            testCycle_log.append(f"[FAIL] {testCase_number} - {testCase}")
        elif "Error" in results:
            testCycle_log.append(f"[ERROR] {testCase_number} - {testCase}")
        else:
            testCycle_log.append(f"[PASS] {testCase_number} - {testCase}")
        
        os.system("clear")
        for log in testCycle_log:
            print(log)

        
        testCase_number += 1

