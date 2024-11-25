from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPlainTextEdit, QVBoxLayout, QWidget,  QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

import sys
 
class Window(QMainWindow):
   def __init__(self, filetext):
      super().__init__()
 
      self.setGeometry(0, 0, 600, 400)
      self.setWindowTitle("Alexa Simulator")

      timer = QtCore.QTimer(self)
      timer.timeout.connect(self.onTimeout)
      timer.start(2000)

      label0 = QLabel(self)
      label0.setText("User Devices")
      label0.setAutoFillBackground(True)
      palette = QPalette()
      palette.setColor(QPalette.Window,Qt.cyan)
      label0.setPalette(palette)
      label0.setAlignment(Qt.AlignCenter)
      label0.resize(300,25)


      self.label1 = QLabel(self)
      self.label1.setText(filetext)
      self.label1.setAutoFillBackground(True)
      palette = QPalette()
      palette.setColor(QPalette.Window,Qt.gray)
      self.label1.setPalette(palette)
      self.label1.setAlignment(Qt.AlignCenter)
      self.label1.resize(300,375)
      self.label1.move(0, 25)
      
      # Create textbox
      self.textbox = QLineEdit(self)
      self.textbox.resize(280,40)
      self.textbox.move(310, 100)
      
        
      # Create a button in the window
      self.button = QPushButton('Send VC', self)
      self.textbox.resize(100,40)
      self.button.move(400,300)
        
      # connect button to function on_click
      self.button.clicked.connect(self.on_click)     


      self.show()

   def onTimeout(self):
      f = open("devices.txt", 'r')
      text = f.read()
      self.label1.setText(text)
      f.close()

   def on_click(self):
      textboxValue = self.textbox.text()
      QMessageBox.question(self, 'Message - ', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
      self.textbox.setText("")
   


app = QApplication(sys.argv)
f = open("devices.txt", 'r')
text = f.read()
f.close()
print(text)


window = Window(text)

sys.exit(app.exec_())