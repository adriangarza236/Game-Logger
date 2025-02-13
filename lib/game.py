from __init__ import CURSOR, CONN


class Game:
    def __init__(self, title, developer, id = None, genre_id = None):
        self.title = title
        self.developer = developer
        self.id = id
        self.genre_id = genre_id

    def __repr__(self):
        return f"Game title: {self.title}, developer: {self.developer}, id: {self.id}, genre_id: {self.genre_id}"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and len(title) > 0:
            self._title = title
        else:
            raise TypeError("Title of videogame must be a string")
        
    @property
    def developer(self):
        return self._developer
    
    @developer.setter
    def developer(self, developer):
        if isinstance(developer, str) and len(developer) > 0:
            self._developer = developer
        else:
            raise TypeError("Developer must be a string")
        
    @property
    def genre(self):
        from genre import Genre
        sql = '''
            SELECT * FROM genres WHERE id = ?
            '''
        row = CURSOR.execute(sql, (self.genre_id,)).fetchone()
        return Genre.create_from_row(row)
    
    @genre.setter
    def genre(self, genre):
        sql = '''
            UPDATE games
            SET genre_id = ?
            WHERE id = ?
            '''
        CURSOR.execute(sql, (genre.id, self.id))
        CONN.commit()

        self.genre_id = genre.id

    
    @classmethod
    def create_table(cls):
        sql = '''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                title TEXT,
                developer TEXT,
                genre_id INTEGER
                );
                '''
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def delete_table(cls):
        sql = "DROP TABLE games;"
        CURSOR.execute(sql)

    def save(self):
        if not self.id:
            sql = '''
                INSERT INTO games (title, developer)
                VALUES (?, ?)
            '''
            CURSOR.execute(sql, (self.title, self.developer))
            CONN.commit()

            sql = '''
            SELECT * FROM games ORDER BY id DESC limit 1
            '''
            id = CURSOR.execute(sql).fetchone()[0]
            self.id = id

    @classmethod
    def create(cls, title, developer, genre_id = None):
        game = cls(title, developer, genre_id)
        game.save()
        return game

    def update(self):
        sql = '''
            UPDATE games
            SET title = ?, developer = ?, genre_id = ?
            WHERE id = ?
            '''
        CURSOR.execute(sql, (self.title, self.developer, self.genre_id, self.id))
        CONN.commit()

    def delete(self):
        sql = '''
            DELETE FROM games
            WHERE id = ?
            '''
        CURSOR.execute(sql, (self.id,))
        CONN.commit()    
        self.id = None

    @classmethod
    def create_from_row(cls, row):
        return Game(id=row[0], title=row[1], developer=row[2], genre_id=row[3])
    
    @classmethod
    def all(cls):
        sql = '''SELECT * FROM games'''
        rows = CURSOR.execute(sql).fetchall()
        return [Game.create_from_row(row) for row in rows]
    
    @classmethod
    def find_by_title(cls, title):
        title = title.lower()
        sql = '''
            SELECT * 
            FROM games
            WHERE LOWER(title) = ?
            '''
        row = CURSOR.execute(sql, (title,)).fetchone()
        return cls.create_from_row(row) if row else None
    
    @classmethod
    def find_by_developer(cls, developer):
        developer = developer.lower()
        sql = '''
            SELECT * 
            FROM games
            WHERE LOWER(developer) = ?
            '''
        rows = CURSOR.execute(sql, (developer,)).fetchall()
        return [Game.create_from_row(row) for row in rows]






