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
    def __init__(self, window, db):
        self.window = window
        self.db = db
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
        self.insert_button.clicked.connect(self.insert)
        container_layout.addWidget(top_row)
        container_layout.addWidget(form_row)
        container_layout.addWidget(self.insert_button)
        container.setLayout(container_layout)
        self.window.setCentralWidget(container)

        #setting up the default initial values
        self.state = "Sighting"
        self.set_form("Name", "Person", "Location", "Sighted")


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
    
    def insert(self):
        # getting the values in each field
        values = [field.text() for field in self.fields]
        if self.state == "Flower":
            self.db.add_flower(*values)
        elif self.state == "Feature":
            self.db.add_feature(*values)
        elif self.state == "Sighting":
            self.db.add_sighting(*values)
        self.window.close()
    
    def show(self):
        self.window.show()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        if "db" in kwargs:
            self.db = kwargs['db']
        else:
            raise Exception("No database supplied")
        del kwargs['db']
        super(MainWindow, self).__init__(*args, **kwargs)
        self.results = None
        self.result_label = "Results: "



        container = QWidget()
        buttons = QWidget()
        layout = QHBoxLayout()

        c_button = QPushButton('+')

        c_button.setStyleSheet('padding: 5px')

        c_button.clicked.connect(self.on_button_clicked_c)

        label = QLabel("Search")
        query = QLineEdit()

        query.textChanged.connect(self.on_text_change)


        layout.addWidget(label)
        layout.addWidget(query)
        layout.addWidget(c_button)        

        self.dialog_create = DialogCreate(SubWindow(self), self.db)
        self.dialog_update = SubWindow(self)
        
        f_layout = QVBoxLayout()


        buttons.setLayout(layout)

        results_container = QWidget()
        results_container.setStyleSheet('padding: 50px')
        self.results_table = QTableWidget()

        # initiate table
        self.results_table.setWindowTitle("Flowers")
        self.results_table.resize(600, 600)
        #results_table.horizontalHeader.hide()
        self.results_table.setRowCount(10)
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["GENUS", "SPECIES", "COMNAME"])

        self.results_table.setObjectName('results')
        

        f_layout.addWidget(buttons)
        f_layout.addWidget(self.results_table)
        container.setLayout(f_layout)

        self.setCentralWidget(container)
        self.setWindowTitle("Flower-Viewer")
        self.show()

    def on_button_clicked_c(self):
        self.dialog_create.show()
    
    def on_combobox_changed(self, value):
        print("Value: ", value)

    def update_table(self, db_results):
        for i, row in enumerate(db_results):
            for j, item in enumerate(row): 
                self.results_table.setItem(i, j, QTableWidgetItem(item))


    def on_text_change(self, value):
        
        self.results_table.clearContents()

        flowers = []

        #Loop through the results and create a label for each flower
        self.update_table(self.db.get_flowers_by_keyword(value))
    
    

        

if __name__ == "__main__":
    flower_db = FlowerDB("test.db")
    with flower_db:
        qApp = QApplication([])
        set_dark_style(qApp)
        window = MainWindow(db=flower_db)
        qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        qApp.exec_()