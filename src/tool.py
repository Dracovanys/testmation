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

    # Interaction commands

    if command.find("TAP") == 0:

        '''
        TAP(x, y) - Tap screen on passed position
        '''

        x = command[command.find("(") + 1:command.find(",")].strip()
        y = command[command.find(",") + 1:command.find(")")].strip()

        # Checking parameters
        try:
            x = float(x)
            y = float(y)
        except:
            result.append("Invalid")
            return

        sentCommand += tap(x, y)

    elif command.find("SWIPE") == 0:

        '''
        SWIPE(x1, y1, x2, y2, *duration) - Do a swipe on screen from x1-y1 position
        to x2-y2 position.

        *This parameter is used to define how much time the swipe process will get
        to complete, it's optional with 1000 milliseconds by default.
        '''

        x1_position = command.find("(") + 1
        x1 = command[x1_position:command.find(",", x1_position)].strip()
        y1_position = command.find(",", x1_position) + 1
        y1 = command[y1_position:command.find(",", y1_position)].strip()
        x2_position = command.find(",", y1_position) + 1
        x2 = command[x2_position:command.find(",", x2_position)].strip()
        y2_position = command.find(",", x2_position) + 1
        y2 = command[y2_position:command.find(",", y2_position)].strip()       

        # Conditional logic in case of user don't give duration
        if command.find(",", y2_position + (len(y2) + 2)) > -1:            
            duration_position = command.find(",", y2_position) + 1
            duration = command[duration_position:command.find(")", duration_position)].strip()

            # Checking parameters
            try:
                x1 = float(x1)
                y1 = float(y1)
                x2 = float(x2)
                y2 = float(y2)
                duration = int(duration)
            except:
                result.append("Invalid")
                return

            # Authorize command
            sentCommand += swipe(x1, y1, x2, y2, duration)

        elif command.find(")", x2_position + (len(x2) + 2)) > -1:
            y2_position = command.find(",", x2_position) + 1
            y2 = command[y2_position:command.find(",", y2_position)].strip()

            # Checking parameters
            try:
                x1 = float(x1)
                y1 = float(y1)
                x2 = float(x2)
                y2 = float(y2)
            except:
                result.append("Invalid")
                return
            
            # Authorize command
            sentCommand += swipe(x1, y1, x2, y2)

    elif command.find("DRAGDROP") == 0:

        '''
        DRAGDROP(x1, y1, x2, y2, duration) - Drag some item on a screen location (x1, y1) and drop it on
        another location (x2, y2) during some milliseconds (duration).
        '''

        x1 = command[command.find("(") + 1:command.find(",")].strip()
        y1 = command[command.find(x1) + (len(x1) + 1):command.find(",", command.find(x1) + (len(x1) + 1))].strip()
        x2 = command[command.find(y1) + (len(y1) + 1):command.find(",", command.find(y1) + (len(y1) + 1))].strip()
        y2 = command[command.find(x2) + (len(x2) + 1):command.find(",", command.find(x2) + (len(x2) + 1))].strip()
        duration = command[command.find(y2) + (len(y2) + 1):command.find(")", command.find(y2) + (len(y2) + 1))].strip()

        # Checking parameters
        try:
            x1 = float(x1)
            y1 = float(y1)
            x2 = float(x2)
            y2 = float(y2)
        except:
            result.append("Invalid")
            return

        sentCommand += dragAndDrop(x1, y1, x2, y2, duration)

    elif command.find("OPEN") == 0:
        
        '''
        OPEN(com.[app].[something]) - Open a specified app.
        '''

        app = command[command.find("(") + 1:command.find(")")].strip()

        # Checking parameters
        if app.find("com.") != 0:
            result.append("Invalid")
            return

        sentCommand += openApp(app)        

    # Verification commands

    elif command.find("COMPARE_IMAGE") == 0:

        '''
        COMPARE_IMAGE(referenceimage.extension, similarityRate; x1, y1, x2, y2) - Compare a printscreen got during
        test execution and compare with a reference printscreen got previously based on a similarity rate (integer number).

        Reference Image should be put on "reference" folder to be used by tool.
        
        OPTIONAL: x1, y1, x2, y2 are float variables (xxxx.x) used just to compare crops of both screens if you want a refined
        comparison.
        '''

        referenceImage = command[command.find("(") + 1:command.find(",")].strip()        

        # Localized
        if command.find(";", command.find(",") + 1) > -1:
            passRate = command[command.find(",") + 1:command.find(";")].strip()

            left_position = command.find(";") + 1
            left = command[left_position:command.find(",", left_position)].strip()
            top_position = command.find(",", left_position) + 1
            top = command[top_position:command.find(",", top_position)].strip()
            right_position = command.find(",", top_position) + 1
            right = command[right_position:command.find(",", right_position)].strip()
            bottom_position = command.find(",", right_position) + 1
            bottom = command[bottom_position:command.find(")", bottom_position)].strip()            
        else:
            passRate = command[command.find(",") + 1:command.find(")")].strip()


        # Checking parameters
        try:
            passRate = float(passRate)

            if not os.path.exists(f"{root}/reference/{referenceImage}"):
                result.append("Invalid")
                return

            if command.find(";", command.find(",") + 1) > -1:
                left = float(left)
                top = float(top)
                right = float(right)
                bottom = float(bottom)
        except:
            result.append("Invalid")
            return

        # Authorize command
        result_folder += f"/capture-image_{datetime.now().day}{datetime.now().month}{datetime.now().year}{datetime.now().hour}{datetime.now().minute}{datetime.now().second}"
        os.mkdir(result_folder)

        sentCommand_ = sentCommand + captureImage()
        validationImage = sentCommand_[sentCommand_.find("/", sentCommand_.find("sdcard")) + 1:]

        os.system(sentCommand_)        

        sentCommand_ = sentCommand + getImage(validationImage, result_folder)

        os.system(sentCommand_)

        # Comparing and giving result       

        # Localized
        if command.find(";", command.find(",") + 1) > -1:
            Image.open(f"{root}/reference/{referenceImage}").crop((int(left), int(top), int(right), int(bottom))).save(f"{result_folder}/expected.png")
            Image.open(f"{result_folder}/{validationImage}").crop((int(left), int(top), int(right), int(bottom))).save(f"{result_folder}/output.png")

            expected = np.array(Image.open(f"{result_folder}/expected.png"))
            output = np.array(Image.open(f"{result_folder}/output.png"))

            try:
                comparison = uqi(expected, output) * 100
            except AssertionError:
                result.append("AssertionError")
                return
            os.remove(f"{result_folder}/{validationImage}")
        
        # Default
        else:       
            expected = np.array(Image.open(f"{root}/reference/{referenceImage}"))
            output = np.array(Image.open(f"{result_folder}/{validationImage}"))

            try:
                comparison = uqi(expected, output) * 100
            except AssertionError:
                result.append("AssertionError")
                return
        
        if comparison >= float(passRate):
            result.append("Pass")
        else:
            result.append("Fail")
        return

    else:
        result.append("Invalid")
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
            result.append("Pass")
            sleep(sleepTime)
    else:
        os.system(sentCommand)
        result.append("Pass")
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
    
    '''
    Start and manage all test cycle
    execution    
    '''

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

        '''
        PASS - All commands executed normally and verifications passed.
        FAIL - At least, 1 command or verification failed.
        INVALID - At least, 1 command or verification have a syntax problem.
        '''

        if "Fail" in results:
            testCycle_log.append(f"[FAIL] {testCase_number} - {testCase}")
        elif "Invalid" in results:
            testCycle_log.append(f"[INVALID] {testCase_number} - {testCase}")
        elif "AssertionError" in results:
            testCycle_log.append(f"[ERROR] {testCase_number} - {testCase} (Reference image haven't the same dimensions of device screen.)")
        else:
            testCycle_log.append(f"[PASS] {testCase_number} - {testCase}")
        
        os.system("clear")
        for log in testCycle_log:
            print(log)
        
        testCase_number += 1

