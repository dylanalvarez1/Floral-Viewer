import sqlite3
import os
from datetime import datetime

class InputError(Exception):
    '''Exception thrown when user makes an error'''
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason

class DatabaseError(Exception):
    '''Exception thrown when database error occurs'''
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason


class FlowerDB:
    '''Wrapper to sqlite3 database'''
    def __init__(self, filename="flowers.db", logfile=None):
        '''Creates the connection and cursor to database at [filename]'''
        assert os.path.exists(filename)
        self.filename = filename
        self.logfile = logfile
        if logfile is None:
            self.logfile = filename.rstrip(".db") + ".log"
        self.loghandle = None
    
    #CONTEXT MANAGEMENT FUNCTIONS
    def __enter__(self):
        '''Establishes a connection upon entry'''
        self.loghandle = open(self.logfile, 'a')
        self._connection = sqlite3.connect(self.filename)
        self._connection.set_trace_callback(self.loghandle.write)
        self._cursor = self._connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        '''Closes the connection upon exit'''
        # commit changes to the database only if no exception
        if exc_type is None and exc_value is None:
            self._connection.commit()
        self._connection.close()
        self.loghandle.close()
    

    # UTILITY FUNCTIONS
    def get_common_names(self):
        '''Returns a list of flowers'''
        self._cursor.execute('''
            SELECT COMNAME FROM FLOWERS 
            ORDER BY COMNAME;''')
        return self._cursor.fetchall()
    
    def get_location_names(self):
        '''Returns a list of locations'''
        self._cursor.execute('''
            SELECT LOCATION FROM FEATURES 
            ORDER BY LOCATION;''')
        return self._cursor.fetchall()

    # QUERY METHODS
    def get_sightings_by_keyword(self, keyword):
        '''Returns a list of sightings filtered by keyword'''
        #if keyword is None:
            #return self.get_sightings()
        self._cursor.execute('''
            SELECT * FROM SIGHTINGS
            WHERE NAME LIKE ? OR PERSON LIKE ? OR LOCATION LIKE ? OR SIGHTED LIKE ?
            ORDER BY SIGHTED DESC''', ('%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%'))
        return self._cursor.fetchall()

    def get_flowers_by_keyword(self, keyword):
        '''Returns a list of flowers filtered by keyword'''
        #if keyword is None:
            #return self.get_flowers()
        self._cursor.execute('''
            SELECT * FROM FLOWERS
            WHERE COMNAME LIKE ? OR GENUS LIKE ? OR SPECIES LIKE ?''', ('%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%'))
        return self._cursor.fetchall()

    def get_features_by_keyword(self, keyword):
        '''Returns a list of flowers filtered by keyword'''
        #if keyword is None:
            #return self.get_location()
        self._cursor.execute('''
            SELECT * FROM FEATURES
            WHERE LOCATION LIKE ? OR CLASS LIKE ? OR LATITUDE LIKE ? OR LONGITUDE LIKE ? OR MAP LIKE ? OR ELEV LIKE ?''',  ("%"+keyword+"%", '%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%'))
        
        return self._cursor.fetchall()    

    def update_flowers(self, old_row, new_row):
        if "" in new_row:
            raise InputError("Field cannot be empty.")
        if new_row[2] != old_row[2] and new_row[2].lower() in [item[0].lower() for item in self.get_common_names()]:
            raise InputError("Flower '%s' already found in the Flowers table." % new_row[2])
        try:
            self._cursor.execute('''
                UPDATE FLOWERS
                SET GENUS = ?, SPECIES = ?, COMNAME = ?
                WHERE GENUS = ? AND SPECIES = ? and COMNAME = ?
                ''', new_row + old_row)
        except sqlite3.IntegrityError:
            raise DatabaseError("Attempted update creates non-unique flower.")

    def update_features(self, old_row, new_row):
        if "" in new_row:
            raise InputError("Field cannot be empty.")
        if new_row[0] != old_row[0] and new_row[0].lower() in [item[0].lower() for item in self.get_location_names()]:
            raise InputError("Location '%s' is already found in the Features table." % new_row[0])
        try:
            float(new_row[2])
            float(new_row[3])
            float(new_row[5])
        except ValueError:
            raise InputError("Latitude, Longitude, and Elev must be numeric.")
        try:
            self._cursor.execute('''
                UPDATE FEATURES
                SET LOCATION = ?, CLASS = ?, LATITUDE = ?, LONGITUDE = ?, MAP = ?, ELEV = ?
                WHERE LOCATION = ? AND CLASS = ? AND LATITUDE = ? AND LONGITUDE = ? AND MAP = ? AND ELEV = ?
                ''', new_row + old_row)
        except sqlite3.IntegrityError:
            raise DatabaseError("Attempted update creates non-unique feature.")
    
    def update_sightings(self, old_row, new_row):
        if "" in new_row:
            raise InputError("Field cannot be empty.")
        if new_row[0] != old_row[0] and new_row[0] not in [item[0] for item in self.get_common_names()]:
            raise InputError("Flower '%s' is not found in the Flowers table." % new_row[0])
        if new_row[2] != old_row[2] and new_row[2] not in [item[0] for item in self.get_location_names()]:
            raise InputError("Location '%s' is not found in the Features table." % new_row[2])
        try:
            datetime.strptime(new_row[3], '%Y-%m-%d')
        except ValueError:
            raise InputError("Incorrect data format, should be YYYY-MM-DD")
        try:
            self._cursor.execute('''
                UPDATE SIGHTINGS
                SET NAME = ?, PERSON =?, LOCATION = ?, SIGHTED = ?
                WHERE NAME = ? AND PERSON = ? AND LOCATION = ? AND SIGHTED = ?
                ''', new_row + old_row)
        except sqlite3.IntegrityError:
            raise DatabaseError("Attempted update creates non-unique sighting.")


    # INSERT FUNCTIONS
    def add_sighting(self, name, person, location, sighted):
        if "" in [name, person, location, sighted]:
            raise InputError("Field cannot be empty.")
        if name not in [item[0] for item in self.get_common_names()]:
            raise InputError("Flower '%s' is not found in the Flowers table." % name)
        if location not in [item[0] for item in self.get_location_names()]:
            raise InputError("Location '%s' is not found in the Features table." % location)
        try:
            datetime.strptime(sighted, '%Y-%m-%d')
        except ValueError:
            raise InputError("Incorrect data format, should be YYYY-MM-DD")
        try:
            self._cursor.execute('''
            INSERT INTO SIGHTINGS
            VALUES(?, ?, ?, ?);
            ''', (name, person, location, sighted))
        except sqlite3.IntegrityError:
            raise DatabaseError("Provided sighting already in table.")
    
    def add_flower(self, genus, species, comname):
        if "" in [comname, genus, species]:
            raise InputError("Field cannot be empty.")
        if comname.lower() in [item[0].lower() for item in self.get_common_names()]:
            raise InputError("Flower '%s' already found in the Flowers table." % comname)
        try:
            self._cursor.execute('''
            INSERT INTO FLOWERS
            VALUES(?, ?, ?);
            ''', (genus, species, comname))
        except sqlite3.IntegrityError:
            raise DatabaseError("Provided flower already in table.")
    
    def add_feature(self, location, loc_class, latitude, longitude, loc_map, elev):
        if "" in [location, loc_class, latitude, longitude, loc_map, elev]:
            raise InputError("Field cannot be empty.")
        if location.lower() in [item[0].lower() for item in self.get_location_names()]:
            raise InputError("Location '%s' is already found in the Features table." % location)
        try:
            float(latitude)
            float(longitude)
            float(elev)
        except ValueError:
            raise InputError("Latitude, Longitude, and Elev must be numeric.")
        try:
            self._cursor.execute('''
            INSERT INTO FEATURES
            VALUES(?, ?, ?, ?, ?, ?);
            ''', (location, loc_class, latitude, longitude, loc_map, elev))
        except sqlite3.IntegrityError:
            raise DatabaseError("Provided feature already in table.")

    #LOGIN/SIGNUP FUNCTIONS 

    def create_user_table(self):
        self._cursor.execute('''
        CREATE TABLE IF NOT EXISTS 
        USERS (username VARCHAR(30) primary key, 
        password VARCHAR(30),
        UNIQUE(USERNAME)
        );
        ''')
    
    def get_all_users(self):
        self._cursor.execute('''
        SELECT username FROM USERS
        ''')
        return self._cursor.fetchall()

    def add_user(self, username, password):
        self._cursor.execute('''
        INSERT OR IGNORE INTO USERS
        VALUES(?, ?);
        ''', (username, password))

    def authenticate_user(self, username, password):
        self._cursor.execute('''
        SELECT USERNAME FROM USERS
        WHERE USERNAME = ? AND PASSWORD = ?
        ;''', (username, password))

        if self._cursor.fetchall() != []:
            self.loghandle.write("\nSuccessfully logged in user '%s'\n" % username)
            return True
        self.loghandle.write("\nFailed to log in user '%s'\n" % username)
        return False
    
    # SQLITE INDEX COMMANDS
    def create_index_for_sightings(self):
        self.create_index_1()
        self.create_index_2()
        self.create_index_3()
        self.create_index_4()
         
    def create_index_1(self):
        self._cursor.execute('''
        CREATE INDEX IF NOT EXISTS sightings_names ON SIGHTINGS (name);
        ''')
    def create_index_2(self):
        self._cursor.execute('''
        CREATE INDEX IF NOT EXISTS sightings_persons ON SIGHTINGS (person);
        ''')
    def create_index_3(self):
        self._cursor.execute('''
        CREATE INDEX IF NOT EXISTS sightings_locations ON SIGHTINGS (location);
        ''')
    def create_index_4(self):
        self._cursor.execute('''
        CREATE INDEX IF NOT EXISTS sightings_sighteds ON SIGHTINGS (sighted);
        ''')

    #SQL TRIGGER COMMANDS
    """ def create_trigger_sightings_insert(self):
        self._cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS sightings_insert AFTER INSERT ON SIGHTINGS
        BEGIN    
        END;
        ''') """
