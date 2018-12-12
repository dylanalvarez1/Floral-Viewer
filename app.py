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

class DialogUpdate():
    def __init__(self, window, db, item, choice, parent):
        self.window = window
        self.db = db
        self.item = item
        self.choice = choice
        self.parent = parent

        container = QWidget()
        container_layout = QVBoxLayout()
        top_row = QWidget()
        top_row_layout = QHBoxLayout()
        label = QLabel('Update entry: ' + self.item.text())
        top_row_layout.addWidget(label)
        top_row.setLayout(top_row_layout)

        form_row = QWidget()
        self.form_row_layout = QFormLayout()
        self.fields = []
        form_row.setLayout(self.form_row_layout)

        self.insert_button = QPushButton("Update")
        self.insert_button.clicked.connect(self.update_clicked)
        container_layout.addWidget(top_row)
        container_layout.addWidget(form_row)
        container_layout.addWidget(self.insert_button)
        container.setLayout(container_layout)
        self.window.setCentralWidget(container)

        #setting up the default initial values
        self.state = self.choice
        self.select_form()


    def set_form(self, *label_names):
        while len(self.form_row_layout) > 0:
            self.form_row_layout.removeRow(0)
        self.fields = []
        for label_name in label_names:
            label = QLabel(label_name)
            field = QLineEdit()
            self.fields.append(field)
            self.form_row_layout.addRow(label, field)
        
    def select_form(self):
        self.state = self.choice
        print('State:', self.choice)
        if self.state == "Flower":
            self.set_form("Genus", "Species", "Common Name (key)")
        elif self.state == "Feature":
            self.set_form("Location", "Class", "Latitude", "Longitude", "Map", "Elev")
        elif self.state == "Sighting":
            self.set_form("Name (key)", "Person", "Location", "Sighted")
        else:
            raise Exception("Unrecognized state:\n%s" % repr(self.state))
    
    def update_clicked(self):
        # getting the values in each field
        values = [field.text() for field in self.fields]
        if self.state == "Flower":
            self.db.update_flower(*values)
        elif self.state == "Feature":
            self.db.update_feature(*values)
        elif self.state == "Sighting":
            self.db.update_sighting(*values)
        self.parent.do_sheet_update()
        self.window.close()
    
    def show(self):
        self.window.show()

class Sheet:
    def __init__(self, title, header, row_count, column_count, query_function, parent):
        self.table = QTableWidget()
        self.table.resize(600, 600)
        self.parent = parent
        self.cell_r = ""
        self.cell_c = ""
        self.table.setRowCount(row_count)
        self.table.setColumnCount(column_count)
        self.table.setHorizontalHeaderLabels(header)

        #Make table not editable
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        #Connect cell clicked event
        self.table.cellClicked.connect(self.cell_was_clicked)

        #Resize rows to fit screen
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.query_function = query_function

    def update(self, search_term="", limit=None):
        results = self.query_function(search_term)
        if limit is not None:
            results = results[:limit]
        #settign Row count to avoid empty rows
        self.table.setRowCount(len(results))
        self.table.clearContents()
        for i, row in enumerate(results):
            for j, item in enumerate(row): 
                self.table.setItem(i, j, QTableWidgetItem(str(item)))
    
    def cell_was_clicked(self, row, column):
        
        print("Row %d and Column %d was clicked" % (row+1, column))
        self.cell_r = row+1
        self.cell_c = column
        item = self.table.item(row, column)
        print(item.text())
        self.parent.create_update_dialog(item)
        self.parent.dialog_update.show()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        if "db" in kwargs:
            self.db = kwargs['db']
        else:
            raise Exception("No database supplied")
        del kwargs['db']
        super(MainWindow, self).__init__(*args, **kwargs)

        container = QWidget()
        buttons = QWidget()
        layout = QHBoxLayout()

        c_button = QPushButton('Create New Entry')

        c_button.setStyleSheet('padding: 5px')

        c_button.clicked.connect(self.on_button_clicked_c)

        self.filter_label = QLabel("Search")
        self.query = QLineEdit()

        self.query.textChanged.connect(self.do_sheet_update)


        layout.addWidget(self.filter_label)
        layout.addWidget(self.query)

         #Create input field that only allows int
        self.onlyInt = QIntValidator()
        self.LineEdit = QLineEdit()
        self.LineEdit.setValidator(self.onlyInt)
        self.LineEdit.setFixedWidth(50)
        self.result_size_label = QLabel("Limit:")

        #Change the value of the result size
        self.result_size = 10
        self.LineEdit.textChanged.connect(self.change_result_size)
        layout.addWidget(self.result_size_label)
        layout.addWidget(self.LineEdit)

        layout.addWidget(c_button)        

        self.dialog_create = DialogCreate(SubWindow(self), self.db)
       
        
        f_layout = QVBoxLayout()

        buttons.setLayout(layout)

        results_container = QWidget()
        results_container.setStyleSheet('padding: 50px')

        # setting up the 3 sheets
        self.sightings_sheet = Sheet("Sightings", ["NAME", "PERSON", "LOCATION", "SIGHTING"], 10, 4, self.db.get_sightings_by_keyword, self)
        self.flowers_sheet = Sheet("Flowers", ["GENUS", "SPECIES", "COMNAME"], 10, 3, self.db.get_flowers_by_keyword, self)
        self.features_sheet = Sheet("Features", ["LOCATION", "CLASS", "LATITUDE", "LONGITUDE", "MAP", "ELEV"], 10, 6, self.db.get_features_by_keyword, self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300,200) 
 
        # Add tabs
        self.tabs.addTab(self.tab1,"Sightings")
        self.tabs.addTab(self.tab2,"Flowers")
        self.tabs.addTab(self.tab3,"Features")

        #layouts for tabs
        self.tab1.layout = QVBoxLayout()
        self.tab1.layout.addWidget(self.sightings_sheet.table)
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout = QVBoxLayout()
        self.tab2.layout.addWidget(self.flowers_sheet.table)
        self.tab2.setLayout(self.tab2.layout)

        self.tab3.layout = QVBoxLayout()
        self.tab3.layout.addWidget(self.features_sheet.table)
        self.tab3.setLayout(self.tab3.layout) 
    
        # calling the sheet update function whenever tab is changed
        self.tabs.currentChanged.connect(self.do_sheet_update)
        # calling sheet_update so the sheet is filled to begin with
        self.do_sheet_update()

        f_layout.addWidget(buttons)

        f_layout.addWidget(self.tabs)
        container.setLayout(f_layout)

        self.setCentralWidget(container)
        self.setWindowTitle("Flower-Viewer")
        self.showMaximized()

    def on_button_clicked_c(self):
        self.dialog_create.show()
    
    def on_combobox_changed(self, value):
        print("Value: ", value)        
    
    def change_result_size(self, value):
        if value:
            self.result_size = int(value)
            print('value:', value)
            self.do_sheet_update()
    
    def getChoice(self, x):
        return {
            0 : "Sighting",
            1 : "Flower",
            2 : "Feature"
        }.get(x, "Sighting")

    def create_update_dialog(self, item):
        choice = self.getChoice(self.tabs.currentIndex())
        print('choice:', choice)
        self.dialog_update = DialogUpdate(SubWindow(self), self.db, item, choice, self)

    def do_sheet_update(self):
        # getting current index
        # 0 = Sightings
        # 1 = Flowers
        # 2 = Features
        index = self.tabs.currentIndex()
        if index == 0:
            sheet = self.sightings_sheet
            self.filter_label.setText("Filter by flower:")
        elif index == 1:
            sheet = self.flowers_sheet
            self.filter_label.setText("Filter by flower:")
        elif index ==2:
            self.filter_label.setText("Filter by location:")
            sheet = self.features_sheet
        else:
            raise Exception("Unrecognized sheet index:\n%s" % index)
        sheet.update(self.query.text(), self.result_size)
        
    
    

        

if __name__ == "__main__":
    flower_db = FlowerDB("test.db")
    with flower_db:
        qApp = QApplication([])
        set_dark_style(qApp)
        window = MainWindow(db=flower_db)
        qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
        qApp.exec_()