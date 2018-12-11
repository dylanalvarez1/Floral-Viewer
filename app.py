from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

qApp = QApplication([])

qApp.setStyle("Fusion")

dark_palette = QPalette()

dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
dark_palette.setColor(QPalette.WindowText, Qt.white)
dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
dark_palette.setColor(QPalette.ToolTipText, Qt.white)
dark_palette.setColor(QPalette.Text, Qt.white)
dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
dark_palette.setColor(QPalette.ButtonText, Qt.white)
dark_palette.setColor(QPalette.BrightText, Qt.red)
dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
dark_palette.setColor(QPalette.HighlightedText, Qt.black)

qApp.setPalette(dark_palette)


def on_button_clicked_c():
    alert = QMessageBox()
    alert.setText('Create a new data entry')
    alert.exec_()

def on_button_clicked_u():
    alert = QMessageBox()
    alert.setText('Update a data entry')
    alert.exec_()


window = QWidget()
layout = QHBoxLayout()

c_button = QPushButton('New')
u_button = QPushButton('Update')

search_area = QWidget()

search_query, ok_pressed = QInputDialog.getText(search_area, "Get text","Search for flowers:", QLineEdit.Normal, "")
if ok_pressed:
    print(search_query)


c_button.setStyleSheet('padding: 5px')

c_button.clicked.connect(on_button_clicked_c)
u_button.clicked.connect(on_button_clicked_u)

layout.addWidget(c_button)
layout.addWidget(u_button)
window.setLayout(layout)
window.show()


qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
qApp.exec_()