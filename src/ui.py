import os
import shutil
from src.commands import captureImage, getImage
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QDesktopWidget, QLabel, QDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QPixmap, QCloseEvent, QPainter, QPen

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

        # Screen View
        self.screenView = QLabel(self)
        self.screenView.setGeometry(30, 30, 589, 740)
        self.screenView.setStyleSheet("border: 1px solid black;")
        self.screenView.mousePressEvent = self.getTapPosition

        # "Open screen" button
        openScreen_btn = QPushButton(self)
        openScreen_btn.setText("Open screen")
        openScreen_btn.setGeometry(650, 30, 320, 40)
        openScreen_btn.clicked.connect(self.openScreen_click)

        # "Get screen" button
        getScreen_btn = QPushButton(self)
        getScreen_btn.setText("Get screen")
        getScreen_btn.setGeometry(650, 85, 320, 40)
        getScreen_btn.clicked.connect(self.getScreen_click)

        # "Save screen" button
        self.saveScreen_btn = QPushButton(self)
        self.saveScreen_btn.setText("Save screen")
        self.saveScreen_btn.setGeometry(650, 140, 320, 40)
        self.saveScreen_btn.clicked.connect(self.saveScreen_click)
        self.saveScreen_btn.setEnabled(False)

        # Interaction info
        self.interactionType_txt = QLabel(self)
        self.interactionType_txt.setGeometry(795, 270, 150, 30)
        self.interactionType_txt.setStyleSheet("font: 20px")

        self.x1Position_txt = QLabel(self)
        self.x1Position_txt.setGeometry(715, 320, 80, 30)

        self.y1Position_txt = QLabel(self)
        self.y1Position_txt.setGeometry(860, 320, 80, 30)

        self.x2Position_txt = QLabel(self)
        self.x2Position_txt.setGeometry(715, 345, 80, 30)

        self.y2Position_txt = QLabel(self)
        self.y2Position_txt.setGeometry(860, 345, 80, 30)

        # Show Device Viewer
        self.show()
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        if os.path.exists(f"{root_path}/temp"):
            shutil.rmtree(f"{root_path}/temp")
        return super().closeEvent(a0)

    def openScreen_click(self):

        '''
        Open a dialog to user choose which screenshot 
        it want to see on Screen Viewer
        '''

        name = QFileDialog.getOpenFileName(self, "Open screen", reference_path, "Screenshot file (*.png)")
        self.screenshot_path = name[0]
        
        if os.path.exists(self.screenshot_path):
            self.showScreen()
            self.saveScreen_btn.setEnabled(False)

    def getScreen_click(self):

        '''
        Take a screenshot from device screen
        and shows it on Screen View
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

        self.showScreen()

        if os.path.exists(self.screenshot_path):
            self.saveScreen_btn.setEnabled(True)

    def saveScreen_click(self):
        dlg = SaveScreen(self.screenshot_path)
    
    def showScreen(self):

        '''
        Scale image on "self.screenshot_path" it order to give
        a proper visualization of it to user
        '''

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

        # Reset interaction info
        self.interactionType_txt.setText("")
        self.x1Position_txt.setText("")
        self.y1Position_txt.setText("")
        self.x2Position_txt.setText("")
        self.y2Position_txt.setText("")        

    def getTapPosition(self, event):

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

            # Draw lines to mark positions
            self.screenView.setPixmap(self.image_adjusted)
            image_draw = self.screenView.pixmap()
            painter = QPainter(image_draw)
            painter.setPen(QPen(Qt.blue, 0.8))

            line_xPosition = event.pos().x() - ((self.screenView.width() - self.image_adjusted.width()) / 2)
            line_yPosition = event.pos().y() - ((self.screenView.height() - self.image_adjusted.height()) / 2)

            painter.drawLine(0, line_yPosition, self.screenView.width(), line_yPosition) # Horizontal line
            painter.drawLine(line_xPosition, 0, line_xPosition, self.screenView.pixmap().height()) # Vertical line
            painter.end()
            self.screenView.setPixmap(image_draw)

            # Show coordinates
            self.interactionType_txt.setText("Tap")
            self.x1Position_txt.setText("X: {:.1f}".format(mouseX_pos))
            self.y1Position_txt.setText("Y: {:.1f}".format(mouseY_pos))
            self.x2Position_txt.setText("")
            self.y2Position_txt.setText("")

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
            screenName = self.screenName_tbox.text()

            if screenName.find("."):
                screenName = screenName.split(".", 1)[0]

            shutil.copyfile(self.screenshot_path, reference_path + f"/{screenName}.png")
            self.close()
        
        