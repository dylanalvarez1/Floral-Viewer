import sqlite3
import os

class FlowerDB:
    def __init__(self, filename="flowers.db"):
        '''Creates the connection and cursor to database at [filename]'''
        assert os.path.exists(filename)
        self.filename = filename
    
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
    
    def get_flowers(self):
        '''Returns a list of flowers'''
        self._cursor.execute('''
            SELECT * FROM FLOWERS 
            ORDER BY COMNAME;''')
        return self._cursor.fetchall()

    def get_flowers_by_keyword(self, keyword):
        '''Returns a list of flowers filtered by keyword'''
        self._cursor.execute('''
            SELECT * FROM SIGHTINGS
            WHERE NAME LIKE \'%''' + keyword + '''%\'
            ORDER BY SIGHTED DESC LIMIT 10''')
        #print(self._cursor.fetchall())
        return self._cursor.fetchall()
    
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

    # TODO: check if comname is a valid file
    def update_flower(self, comname, genus, species):
        self._cursor.execute('''
            UPDATE FLOWERS
            SET GENUS = ?, SPECIES = ?
            WHERE COMNAME = ?
            ''', (genus, species, comname)) 
    
    # TODO: add other updates
    def add_sighting(self, name, person, location, sighted):
        self._cursor.execute('''
        INSERT INTO SIGHTINGS
        VALUES(?, ?, ?, ?);
        ''', (name, person, location, sighted))
        


if __name__ == "__main__":
    flower_db = FlowerDB("test.db")
    with flower_db:
        for flower in flower_db.get_flowers_by_keyword(input()):
            print("%s (%s %s)" % (flower[2], flower[0], flower[1]) )
        