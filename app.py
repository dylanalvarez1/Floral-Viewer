from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import * 
from FlowerDB import FlowerDB

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


class DialogCreate():
    def __init__(self, window):
        self.window = window
        container = QWidget()
        container_layout = QVBoxLayout()
        top_row = QWidget()
        top_row_layout = QHBoxLayout()
        label = QLabel('Create a new')
        self.combo_box = QComboBox()
        self.combo_box.addItem('Sighting')
        self.combo_box.addItem('Flower')
        self.combo_box.addItem('Feature')
        self.combo_box.currentTextChanged.connect(self.update)
        top_row_layout.addWidget(label)
        top_row_layout.addWidget(self.combo_box)
        top_row.setLayout(top_row_layout)

        form_row = QWidget()
        self.form_row_layout = QFormLayout()
        self.fields = []
        form_row.setLayout(self.form_row_layout)

        self.insert_button = QPushButton("Insert")
        container_layout.addWidget(top_row)
        container_layout.addWidget(form_row)
        container_layout.addWidget(self.insert_button)
        container.setLayout(container_layout)
        self.window.setCentralWidget(container)
        self.state = "Sighting"

    def set_form(self, *label_names):
        while len(self.form_row_layout) > 0:
            self.form_row_layout.removeRow(0)
        self.fields = []
        for label_name in label_names:
            label = QLabel(label_name)
            field = QLineEdit()
            self.fields.append(field)
            self.form_row_layout.addRow(label, field)
        
    def update(self):
        self.state = self.combo_box.currentText()
        if self.state == "Flower":
            self.set_form("Genus", "Species", "Common Name")
        elif self.state == "Feature":
            self.set_form("Location", "Class", "Latitude", "Longitude", "Map", "Elev")
        elif self.state == "Sighting":
            self.set_form("Name", "Person", "Location", "Sighted")
        else:
            raise Exception("Unrecognized state:\n%s" % repr(self.state))
        self.show()
    
    def insert():
        if self.state == "Flower":
            # insert into flowers sheet, sanitize where appropriate
            pass
        elif self.state == "Feature":
            # insert into features sheet, sanitize where appropriate
            pass
        elif self.state == "Sighting":
            # insert into sighting sheet, sanitize where appropriate
            pass

    def show(self):
        self.window.show()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.db = None
        self.results = None
        self.result_label = "Results: "


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
        self.dialog_create = DialogCreate(SubWindow(self))
        self.dialog_update = SubWindow(self)
        
        #=====
        f_layout = QVBoxLayout()


        buttons.setLayout(layout)

        results_container = QWidget()
        results_container.setStyleSheet('padding: 200px')
        results_label = QLabel(self.result_label)
        results_label.setObjectName('results')
        

        f_layout.addWidget(buttons)
        f_layout.addWidget(results_label)
        container.setLayout(f_layout)

        self.setCentralWidget(container)
        self.show()

    def set_db(self, db):
        self.db = db

    def on_button_clicked_c(self):
        self.dialog_create.show()
    
    def on_button_clicked_u(self):
        self.dialog_update.show()
    def on_combobox_changed(self, value):
        print("Value: ", value)
    def on_text_change(self, value):
        #self.results = self.db.get_flowers_by_keyword(value)
        self.result_label = "Results: "
        flower_str = ""
        #Loop through the results and create a label for each flower
        for flower in self.db.get_flowers_by_keyword(value):
           flower_str += " %s (%s %s) \n" % (flower[2], flower[0], flower[1])
        self.result_label += flower_str

        #Find the old results
        result_text = self.findChild(QLabel, "results")
        result_text.setText(self.result_label)
    

        

if __name__ == "__main__":
    flower_db = FlowerDB("test.db")
    with flower_db:
        qApp = QApplication([])
        set_dark_style(qApp)
        window = MainWindow()
        window.set_db(flower_db)
        qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        qApp.exec_()