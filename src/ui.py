import os
import shutil
from src.commands import captureImage, getImage
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QDesktopWidget, QLabel, QDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QCloseEvent

root_path = os.getcwd()
reference_path = f"{root_path}/reference"

class DeviceViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Device Viewer")
        self.setFixedSize(1000, 800)

        # Moving to center
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        # "Get screen" button
        getScreen_btn = QPushButton(self)
        getScreen_btn.setText("Get screen")
        getScreen_btn.setGeometry(650, 90, 320, 40)
        getScreen_btn.clicked.connect(self.getScreen_click)

        # "Save screen" button
        self.saveScreen_btn = QPushButton(self)
        self.saveScreen_btn.setText("Save screen")
        self.saveScreen_btn.setGeometry(650, 145, 320, 40)
        self.saveScreen_btn.clicked.connect(self.saveScreen_click)
        self.saveScreen_btn.setEnabled(False)

        # Screen View
        self.screenView = QLabel(self)
        self.screenView.setGeometry(30, 30, 589, 740)
        self.screenView.setStyleSheet("border: 1px solid black;")
        self.screenView.mousePressEvent = self.getCoordinates

        # Show Device Viewer
        self.show()
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        if os.path.exists(f"{root_path}/temp"):
            shutil.rmtree(f"{root_path}/temp")
        return super().closeEvent(a0)

    def getScreen_click(self):

        '''
        Take a screenshot from device screen
        and shows on Screen View
        '''        

        command = f"adb {captureImage()}"
        self.screenshot = command[command.find("/", command.find("sdcard")) + 1:]
        os.system(command)

        temp_path = f"{root_path}/temp"
        if os.path.exists(root_path + "/temp"):
            shutil.rmtree(temp_path)
            os.mkdir(f"{root_path}/temp")
        else:
            os.mkdir(f"{root_path}/temp")

        command = f"adb {getImage(self.screenshot, temp_path)}"
        os.system(command)

        self.screenshot_path = f"{temp_path}/{self.screenshot}"
        
        self.image = QPixmap(self.screenshot_path)

        # Scale screenshot according with Screen View size
        scaled_width = self.image.width()
        scaled_height = self.image.height()
        self.reductionPct= 0
        while scaled_width > self.screenView.width() or scaled_height > self.screenView.height():
            scaled_width -= self.image.width() * 0.01
            scaled_height -= self.image.height() * 0.01
            self.reductionPct += 1

        self.reductionPct /= 100
        self.image_adjusted = self.image.scaled(int(scaled_width), int(scaled_height))

        # print(f"Image Dimensions: [Original: {self.image.width()}x{self.image.height()}] [Scaled: {self.image_adjusted.width()}x{self.image_adjusted.height()}] " +  "[Reduction: {:.1f}%]".format(self.reductionPct * 100))
       
        self.screenView.setPixmap(self.image_adjusted)
        # print(f"Screen View: {self.screenView.width()}x{self.screenView.height()} / Image: {self.image_adjusted.width()}x{self.image_adjusted.height()}")
        self.screenView.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if os.path.exists(self.screenshot_path):
            self.saveScreen_btn.setEnabled(True)

    def saveScreen_click(self):
        dlg = SaveScreen(self.screenshot_path)
    
    def getCoordinates(self, event):

        '''
        Return mouse position on screenshot considering
        its scale.
        '''

        if self.screenView.pixmap() != None:

            mouseX_pos = event.pos().x() / (1 - self.reductionPct) 
            mouseX_pos -= ((self.screenView.width() - self.image_adjusted.width()) / (1 - self.reductionPct)) / 2

            if mouseX_pos < 0:
                mouseX_pos = 0
            elif mouseX_pos > self.image.width():
                mouseX_pos = self.image.width()

            mouseY_pos = event.pos().y() / (1 - self.reductionPct) 
            mouseY_pos -= ((self.screenView.height() - self.image_adjusted.height()) / (1 - self.reductionPct)) / 2

            if mouseY_pos < 1:
                mouseY_pos = 0
            elif mouseY_pos > self.image.height():
                mouseY_pos = self.image.height()

            print("{:.1f}, {:.1f}".format(mouseX_pos, mouseY_pos))

class SaveScreen(QDialog):
    def __init__(self, screenshot_path):
        super().__init__()
        self.setWindowTitle("Save screen")
        self.setFixedSize(400, 200)

        # Moving to center
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Description text
        description_lbl = QLabel(self)
        description_lbl.setText("Choose a name to set on screenshot before save it on \nreference folder.")
        description_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_lbl.setGeometry(12, 8, 376, 30)

        # "Screen Name" label
        screenName_lbl = QLabel(self)
        screenName_lbl.setText("Screenshot name")
        screenName_lbl.setGeometry(12, 65, 200, 30)

        # "Screen Name" text box
        self.screenName_tbox = QLineEdit(self)
        self.screenName_tbox.setGeometry(130, 65, 250, 30)

        # Warning text
        warning_lbl = QLabel(self)
        warning_lbl.setText("*Image will be saved as PNG.")
        warning_lbl.setStyleSheet("font: 10px")
        warning_lbl.setGeometry(130, 90, 376, 30)

        # "Save" button
        save_btn = QPushButton(self)
        save_btn.setText("Save")
        save_btn.setGeometry(155, 160, 80, 30)
        self.screenshot_path = screenshot_path
        save_btn.clicked.connect(self.save_click)
        
        # Show dialog
        self.exec()
        
    def save_click(self):
        if self.screenName_tbox.text() != "":
            shutil.copyfile(self.screenshot_path, reference_path + f"/{self.screenName_tbox.text()}.png")
            self.close()
        
        