from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import * 

def set_dark_style(q_app):
    q_app.setStyle("Fusion")
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
    

        #do something
        #do_loop = False

class SubWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        container = QWidget()
        buttons = QWidget()
        layout = QHBoxLayout()

        c_button = QPushButton('New')
        u_button = QPushButton('Update')

        c_button.setStyleSheet('padding: 5px')

        c_button.clicked.connect(self.on_button_clicked_c)
        u_button.clicked.connect(self.on_button_clicked_u)

        label = QLabel("Search")
        query = QLineEdit()

        query.textChanged.connect(self.on_text_change)


        layout.addWidget(label)
        layout.addWidget(query)
        layout.addWidget(c_button)
        layout.addWidget(u_button)
        #=====
        self.dialog_create = SubWindow(self)
        self.dialog_update = SubWindow(self)
        container_create = QWidget()
        form = QHBoxLayout()

        label = QLabel('Create New ')

        input1 = QComboBox()
        input1.addItem('Flowers')
        input1.addItem('Sightings')
        input1.addItem('Features')

        input1.currentTextChanged.connect(self.on_combobox_changed)

        ok_button = QPushButton('ok')

        form.addWidget(label)
        form.addWidget(input1)    
        container_create.setLayout(form)
        self.dialog_create.setCentralWidget(container_create)
        #=====
        f_layout = QVBoxLayout()


        buttons.setLayout(layout)

        results_container = QWidget()
        results_container.setStyleSheet('padding: 200px')
        results_label = QLabel('Results:')

        f_layout.addWidget(buttons)
        f_layout.addWidget(results_label)
        container.setLayout(f_layout)

        self.setCentralWidget(container)
        self.show()

    def on_button_clicked_c(self):
        self.dialog_create.show()
    
    def on_button_clicked_u(self):
        self.dialog_update.show()
    def on_combobox_changed(self, value):
        print("Value: ", value)
    def on_text_change(self, value):
        print("Current Text: ", value)

        

if __name__ == "__main__":
    qApp = QApplication([])
    set_dark_style(qApp)
    window = MainWindow()
    qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    qApp.exec_()