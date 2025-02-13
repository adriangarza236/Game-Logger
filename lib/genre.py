from __init__ import CURSOR, CONN


class Genre:
    def __init__(self, name, id = None):
        self.name = name
        self.id = id

    def __repr__(self):
        return f"Genre: {self.name}, id: {self.id}"

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 1:
            self._name = name
        else:
            raise TypeError("Genre must be a string")
        
    @property
    def games(self):
        from game import Game
        sql = '''
            SELECT * FROM games WHERE genre_id = (?)
            '''
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Game.create_from_row(row) for row in rows]
        
    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS genres (
                id INTEGER PRIMARY KEY,
                name TEXT
                );
                '''
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def delete_table(cls):
        sql = "DROP TABLE genres;"
        CURSOR.execute(sql)
            
    def save(self):
        if not self.id:
            sql = '''
                INSERT INTO genres (name)
                VALUES (?)
                '''
            CURSOR.execute(sql, (self.name,))
            CONN.commit()

            sql = '''
            SELECT * FROM genres ORDER BY id DESC limit 1 
            '''
            id = CURSOR.execute(sql).fetchone()[0]
            self.id = id

    @classmethod
    def create(cls, name):
        genre = cls(name)
        genre.save()
        return genre
    
    def update(self):
        sql = '''
            UPDATE genres
            SET name = ?
            WHERE id = ?
            '''
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    def delete(self):
        for game in self.games:
            game.delete()
        sql = '''
            DELETE FROM genres
            WHERE id = ?
            '''
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        self.id = None


    @classmethod
    def create_from_row(cls, row):
        return Genre(id=row[0], name=row[1])
    
    @classmethod
    def all(cls):
        sql = '''SELECT * FROM genres'''
        rows = CURSOR.execute(sql).fetchall()
        return [Genre.create_from_row(row)for row in rows]
    
    @classmethod
    def find_by_name(cls, name):
        name= name.lower()
        sql = '''
            SELECT * 
            FROM genres
            WHERE LOWER(name) = ?
            '''
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.create_from_row(row) if row else None
    
    @classmethod
    def find_by_id(cls, id):
        sql = '''
            SELECT * FROM genres WHERE id = ?
            '''
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            return cls.create_from_row(row)
        else:
            return None
