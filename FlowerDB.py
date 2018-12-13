import sqlite3
import os

class FlowerDB:
    def __init__(self, filename="flowers.db"):
        '''Creates the connection and cursor to database at [filename]'''
        assert os.path.exists(filename)
        self.filename = filename
    
    #CONTEXT MANAGEMENT FUNCTIONS
    def __enter__(self):
        '''Establishes a connection upon entry'''
        self._connection = sqlite3.connect(self.filename)
        self._cursor = self._connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        '''Closes the connection upon exit'''
        # commit changes to the database only if no exception
        if exc_type is None and exc_value is None:
            self._connection.commit()
        self._connection.close()
    

    # UTILITY FUNCTIONS
    def get_common_names(self):
        '''Returns a list of flowers'''
        self._cursor.execute('''
            SELECT * FROM FLOWERS 
            ORDER BY COMNAME;''')
        return self._cursor.fetchall()
    
    def get_location_names(self):
        '''Returns a list of locations'''
        self._cursor.execute('''
            SELECT LOCATION FROM FEATURES 
            ORDER BY LOCATION;''')
        return self._cursor.fetchall()


    #QUERY FUNCTIONS
    #POSSIBLY OBSOLETE   
    def get_sightings(self, flower = None):
        if flower is None:
            self._cursor.execute('''
            SELECT * FROM SIGHTINGS
            ORDER BY SIGHTED DESC''')
        else:
            self._cursor.execute('''
                SELECT * FROM SIGHTINGS
                WHERE NAME = ?
                ORDER BY SIGHTED DESC''', (flower,) )
        return self._cursor.fetchall()

    def get_sightings_by_keyword(self, keyword):
        '''Returns a list of sightings filtered by keyword'''
        #if keyword is None:
            #return self.get_sightings()
        self._cursor.execute('''
            SELECT * FROM SIGHTINGS
            WHERE NAME LIKE ?
            ORDER BY SIGHTED DESC''', ('%'+keyword+'%',))
        return self._cursor.fetchall()

    def get_flowers_by_keyword(self, keyword):
        '''Returns a list of flowers filtered by keyword'''
        #if keyword is None:
            #return self.get_flowers()
        self._cursor.execute('''
            SELECT * FROM FLOWERS
            WHERE COMNAME LIKE ?''', ('%'+keyword+'%',))
        return self._cursor.fetchall()

    def get_features_by_keyword(self, keyword):
        '''Returns a list of flowers filtered by keyword'''
        #if keyword is None:
            #return self.get_location()
        self._cursor.execute('''
            SELECT * FROM FEATURES
            WHERE LOCATION LIKE ?''',  ("%"+keyword+"%",))
        
        return self._cursor.fetchall()    

    # TODO: error checking
    # UPDATE FUNCTIONS
    def update_flowers(self, old_row, new_row):
        print(old_row)
        print(new_row)
        self._cursor.execute('''
            UPDATE FLOWERS
            SET GENUS = ?, SPECIES = ?, COMNAME = ?
            WHERE GENUS = ? AND SPECIES = ? and COMNAME = ?
            ''', new_row + old_row)

    def update_features(self, old_row, new_row):
        self._cursor.execute('''
            UPDATE FEATURES
            SET LOCATION = ?, CLASS = ?, LATITUDE = ?, LONGITUDE = ?, MAP = ?, ELEV = ?
            WHERE LOCATION = ? AND CLASS = ? AND LATITUDE = ? AND LONGITUDE = ? AND MAP = ? AND ELEV = ?
            ''', new_row + old_row)
    
    def update_sightings(self, old_row, new_row):
        self._cursor.execute('''
            UPDATE SIGHTINGS
            SET NAME = ?, PERSON =?, LOCATION = ?, SIGHTED = ?
            WHERE NAME = ? AND PERSON = ? AND LOCATION = ? AND SIGHTED = ?
            ''', new_row + old_row)


    # INSERT FUNCTIONS
    # TODO: ADD ERROR CHECKING
    def add_sighting(self, name, person, location, sighted):
        self._cursor.execute('''
        INSERT INTO SIGHTINGS
        VALUES(?, ?, ?, ?);
        ''', (name, person, location, sighted))
    
    def add_flower(self, comname, genus, species):
        self._cursor.execute('''
        INSERT INTO FLOWERS
        VALUES(?, ?, ?);
        ''', (genus, species, comname))
    
    def add_feature(self, location, loc_class, latitude, longitude, loc_map, elev):
        self._cursor.execute('''
        INSERT INTO FEATURES
        VALUES(?, ?, ?, ?, ?, ?);
        ''', (self, location, loc_class, latitude, longitude, loc_map, elev))

    #LOGIN/SIGNUP FUNCTIONS 

    def create_user_table(self):
        self._cursor.execute('''
        CREATE TABLE IF NOT EXISTS 
        USERS (USERNAME VARCHAR(30) primary key, 
        PASSWORD VARCHAR(30));
        ''')
    
    def get_all_users(self):
        self._cursor.execute('''
        SELECT USERNAME FROM USERS
        ''')
        return self._cursor.fetchall()

    def add_user(self, username, password):
        self._cursor.execute('''
        INSERT INTO USERS
        VALUES(?, ?);
        ''', (username, password))

    def authenticate_user(self, username, password):
        self._cursor.execute('''
        SELECT USERNAME FROM USERS
        WHERE USERNAME = ? AND PASSWORD = ?
        ;''', (username, password))

        if self._cursor.fetchall() != []:
            print(self._cursor.fetchall())
            return True
        return False
    
    # SQLITE INDEX COMMANDS
    def create_index_for_sightings(self):
        self._cursor.execute('''
        CREATE INDEX IF NOT EXISTS sightings_names ON SIGHTINGS (name);
        CREATE INDEX IF NOT EXISTS sightings_persons ON SIGHTINGS (person);
        CREATE INDEX IF NOT EXISTS sightings_locations ON SIGHTINGS (location);
        CREATE INDEX IF NOT EXISTS sightings_sighteds ON SIGHTINGS (siighted);
        ''')



if __name__ == "__main__":
    flower_db = FlowerDB("test.db")
    with flower_db:
        #flower_db.update_flowers("Sheltons violet", "ViolaNew", "sheltoniiNew")
        flower_db.create_user_table()
        #flower_db.add_user("test4", "123")
        array = flower_db.get_all_users()
        printstr = ""

        exists = flower_db.authenticate_user("test2", "44")
        if exists:
            print('User is in database\n')
        else:
            print('User is not in database\n')

        for i, row in enumerate(array):
            for j, item in enumerate(row): 
                printstr += str(item) + " "
        print(printstr)