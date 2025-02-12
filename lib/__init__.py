import sqlite3 


CONN = sqlite3.connect("game_logger.db")
CURSOR = CONN.cursor()
