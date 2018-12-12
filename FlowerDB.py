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

    # TODO: check if comname is a valid file
    # UPDATE FUNCTIONS
    def update_flower(self, genus, species, comname):
        self._cursor.execute('''
            UPDATE FLOWERS
            SET GENUS = ?, SPECIES = ?
            WHERE COMNAME = ?
            ''', (genus, species, comname)) 
    



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
        


if __name__ == "__main__":
    flower_db = FlowerDB("test.db")
    with flower_db:
        flower_db.update_flower("Sheltons violet", "ViolaNew", "sheltoniiNew")
        