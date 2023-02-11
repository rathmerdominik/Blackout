import json
import sqlite3

def create_db_conn(db_path: str) -> sqlite3.Connection:
    """Creates a database connection and returns the connection.
    Also creates a database with the required "" table in case it does not exist
    Returns:
        sqlite3.Connection: The created connection
    """
    conn = sqlite3.connect(db_path)

	#Yeah i know about the "artists" thing not being normalized and stuff...
    conn.execute(
        """CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY, 
            title TEXT, 
            artists TEXT, 
            album TEXT,
            year INTEGER,
            total_tracks INTEGER,
            filepath TEXT
        )"""
    )

    return conn

def write_track(conn: sqlite3.Connection, title: str, artists: str, album: str, year: int, total_tracks: int, filepath: str):
    with conn:
        sql = "INSERT INTO tracks (title, artists, album, year, total_tracks, filepath) VALUES(?, ?, ?, ?, ?, ?)"
        conn.execute(sql, (title, artists, album, year, total_tracks, filepath))
        conn.commit()

def get_tracks(conn: sqlite3.Connection):
    with conn:
        db = conn.cursor()
        
        sql = "SELECT * FROM tracks"
        
        return db.execute(sql).fetchall()
        
        
		
        
		