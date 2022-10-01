from PyQt5.QtWidgets import QApplication
from src.ui import *

# Execute app
app = QApplication([])
deviceViewer = DeviceViewer()
app.exec()