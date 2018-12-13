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


class DialogUpdate:
    def __init__(self, sheet_type, item_row, editable_col, window, db, parent_window):
        # not a scalable way of doing this
        self.type = sheet_type.rstrip("s")
        self.window = window
        self.db = db
        self.item_row = item_row
        self.editable_col = editable_col
        self.parent_window = parent_window

        container = QWidget()
        container_layout = QVBoxLayout()
        top_row = QWidget()
        top_row_layout = QHBoxLayout()
        label = QLabel('Updating %s' % sheet_type)
        top_row_layout.addWidget(label)
        top_row.setLayout(top_row_layout)

        form_row = QWidget()
        self.form_row_layout = QFormLayout()
        self.fields = []
        form_row.setLayout(self.form_row_layout)

        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_pressed)
        container_layout.addWidget(top_row)
        container_layout.addWidget(form_row)
        container_layout.addWidget(self.update_button)
        container.setLayout(container_layout)
        self.window.setCentralWidget(container)
        self.build_form()

    
    def set_form(self, *label_names):
        while len(self.form_row_layout) > 0:
            self.form_row_layout.removeRow(0)
        self.fields = []
        noneditable = QPalette()
        noneditable.setColor(QPalette.Base, QColor(53, 53, 53))
        for col, label_name in enumerate(label_names):
            label = QLabel(label_name)
            field = QLineEdit()
            if col != self.editable_col:
                field.setReadOnly(True)
                field.setPalette(noneditable)
            field.setText(self.item_row[col])
            self.fields.append(field)
            self.form_row_layout.addRow(label, field)

    def build_form(self):
        if self.type == "Flower":
            self.set_form("Genus", "Species", "Common Name")
        elif self.type == "Feature":
            self.set_form("Location", "Class", "Latitude", "Longitude", "Map", "Elev")
        elif self.type == "Sighting":
            self.set_form("Name", "Person", "Location", "Sighted")
        else:
            raise Exception("Unrecognized state:\n%s" % repr(self.type))
    
    def update_pressed(self):
        print("update pressed")
        new_values = [field.text() for field in self.fields]
        if self.type == "Flower":
            self.db.update_flowers(self.item_row, new_values)
        elif self.type == "Feature":
            self.db.update_features(self.item_row, new_values)
        elif self.type == "Sighting":
            self.db.update_sightings(self.item_row, new_values)
        else:
            raise Exception("Unrecognized state:\n%s" % repr(self.type))
        self.parent_window.do_sheet_update()
        self.window.close()

class DialogFlowerList:
    def __init__(self, window, db, parent_window):
        # not a scalable way of doing this
        self.window = window
        self.db = db
        self.parent_window = parent_window

        #Do not pass a title to the sheet so it knows how to handle the click behavior
        self.flowers_sheet = Sheet("", ["GENUS", "SPECIES", "COMNAME"], 10, 3, self.db.get_flowers_by_keyword, self)
        self.table = self.flowers_sheet.table

        container = QWidget()
        container_layout = QVBoxLayout()
        top_row = QWidget()
        top_row_layout = QHBoxLayout()
        label = QLabel('Select a flower to search by:')
        top_row_layout.addWidget(label)
        top_row.setLayout(top_row_layout)

        form_row = QWidget()
        self.form_row_layout = QFormLayout()

        self.form_row_layout.addWidget(self.table)
        
        form_row.setLayout(self.form_row_layout)

        container_layout.addWidget(top_row)
        container_layout.addWidget(form_row)
        container.setLayout(container_layout)
        self.window.setCentralWidget(container)
        #update entries
        self.update()

    def update(self, limit=None):
        results = self.db.get_common_names()
        if limit is not None:
            results = results[:limit]
        #settign Row count to avoid empty rows
        self.table.setRowCount(len(results))
        self.table.clearContents()
        for i, row in enumerate(results):
            for j, item in enumerate(row): 
                self.table.setItem(i, j, QTableWidgetItem(str(item)))
    
    #its called this, but it actually puts the text into
    def create_update_dialog(self, sheet_type, item_row, col_num):
        item = self.table.item(item_row, col_num)
        self.parent_window.query.setText(item.text())
        
   
class Sheet:
    def __init__(self, title, header_labels, row_count, column_count, query_function, parent):
        self.title = title
        self.table = QTableWidget()
        self.table.resize(600, 600)
        self.parent = parent
        self.cell_r = ""
        self.cell_c = ""
        self.table.setRowCount(row_count)
        self.table.setColumnCount(column_count)
        self.table.setHorizontalHeaderLabels(header_labels)
        self.header_labels = header_labels

        #Make table not editable
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        #Connect cell clicked event
        self.table.cellClicked.connect(self.cell_was_clicked)

        #Resize rows to fit screen
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
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
        #Sorry Will, I know its bad but this is the only way atm i could find a way to tell if this was called from the flower list or the normal tabs
        if self.title is not "":
            print("Row %d and Column %d was clicked" % (row+1, column))
            self.cell_r = row+1
            self.cell_c = column
            item = self.table.item(row, column)
            item_row = [self.table.item(self.cell_r - 1, i).text() for i in range(self.table.columnCount())]
            # the self.title is the worst way to store the state... using an enum would be better
            self.parent.create_update_dialog(self.title, item_row, self.cell_c)
        
        else:
            #Set the label of self.query (the search bar) to what you clicked
            self.parent.parent_window.query.setText(self.table.item(row, column).text())

class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        
        self.label_user = QLabel("Username: ")
        self.label_pass = QLabel("Password: ")
        self.text_name = QLineEdit(self)
        self.text_pass = QLineEdit(self)
        self.button_login = QPushButton('Login', self)
        self.button_login.clicked.connect(self.handle_login)
        layout = QVBoxLayout(self)
        
        top_row = QWidget()
        top_row_layout = QHBoxLayout()
        top_row_layout.addWidget(self.label_user)
        top_row_layout.addWidget(self.text_name)
        top_row.setLayout(top_row_layout)

        bot_row = QWidget()
        bot_row_layout = QHBoxLayout()
        bot_row_layout.addWidget(self.label_pass)
        bot_row_layout.addWidget(self.text_pass)
        bot_row.setLayout(bot_row_layout)

        title = QLabel("Login to an account to access database manager")

        layout.addWidget(title)
        layout.addWidget(top_row)
        layout.addWidget(bot_row)
        layout.addWidget(self.button_login)


    def handle_login(self):
        if (self.text_name.text() == 'foo' and
            self.text_pass.text() == 'bar'):
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Error', 'Bad user or password')

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        if "db" in kwargs:
            self.db = kwargs['db']
        else:
            raise Exception("No database supplied")
        del kwargs['db']
        super(MainWindow, self).__init__(*args, **kwargs)

        #Window icon
        app_icon = QIcon()
        app_icon.addFile('icon.png')
        self.setWindowIcon(app_icon)

        container = QWidget()
        buttons = QWidget()
        layout = QHBoxLayout()

        c_button = QPushButton('Create New Entry')
        c_button.setStyleSheet('padding: 5px')
        c_button.clicked.connect(self.on_button_clicked_c)

        self.l_button = QPushButton('Select a flower')
        self.l_button.setStyleSheet('padding: 5px')
        self.l_button.clicked.connect(self.on_button_clicked_l)

        self.filter_label = QLabel("Search")
        self.query = QLineEdit()

        self.query.textChanged.connect(self.do_sheet_update)


        layout.addWidget(self.filter_label)
        layout.addWidget(self.query)

        #Create input field that only allows int
        self.limit_box = QLineEdit()
        self.limit_box.setValidator(QIntValidator())
        self.limit_box.setFixedWidth(50)
        self.limit_label = QLabel("Limit:")

        #Change the value of the result size
        self.limit_size = 10
        self.limit_box.textEdited.connect(self.update_limit)
        self.limit_box.setText("10")
        layout.addWidget(self.limit_label)
        layout.addWidget(self.limit_box)

        layout.addWidget(self.l_button)
        layout.addWidget(c_button)        

        self.dialog_create = DialogCreate(SubWindow(self), self.db)
        self.dialog_update = None
        
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
        self.setWindowTitle("Floral-Viewer")
        self.showMaximized()

    def on_button_clicked_c(self):
        self.dialog_create.show()
    
    def on_button_clicked_l(self):
        self.dialog_flower_list = DialogFlowerList(SubWindow(self), self.db, self)
        self.dialog_flower_list.window.show()
    
    def create_update_dialog(self, sheet_type, item_row, col_num):
        # close the old dialog_update window?
        self.dialog_update = DialogUpdate(sheet_type, item_row, col_num, SubWindow(self), self.db, self)
        self.dialog_update.window.show()
    
    def on_combobox_changed(self, value):
        print("Value: ", value)        
    
    def update_limit(self, value):
        print('value:', value)
        if value:
            self.limit_size = int(value)
        else:
            self.limit_size = None
        self.do_sheet_update()
    
    def getChoice(self, x):
        return {
            0 : "Sighting",
            1 : "Flower",
            2 : "Feature"
        }.get(x, "Sighting")


    def do_sheet_update(self):
        # getting current index
        # 0 = Sightings
        # 1 = Flowers
        # 2 = Features
        index = self.tabs.currentIndex()
        if index == 0:
            sheet = self.sightings_sheet
            self.filter_label.setText("Filter by sighting:")
            self.l_button.show()
            self.dialog_create.state = "Sighting"
        elif index == 1:
            sheet = self.flowers_sheet
            self.filter_label.setText("Filter by flower:")
            self.l_button.hide()
            self.dialog_create.state = "Flower"
        elif index ==2:
            self.filter_label.setText("Filter by location:")
            sheet = self.features_sheet
            self.l_button.hide()
            self.dialog_create.state = "Feature"
        else:
            raise Exception("Unrecognized sheet index:\n%s" % index) 
        sheet.update(self.query.text(), self.limit_size)
        
    
    

        

if __name__ == "__main__":
    flower_db = FlowerDB("test.db")
    with flower_db:
        qApp = QApplication([])
        set_dark_style(qApp)
        login = Login()
        if login.exec_() == QDialog.Accepted:
            main_window = MainWindow(db=flower_db)
            qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
            qApp.exec_()