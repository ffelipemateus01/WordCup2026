import sqlite3
from datetime import datetime

class DBProxy:
    def __init__(self, db_name: str = 'wordcup.db'):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.connection.execute('''
                                   CREATE TABLE IF NOT EXISTS winners(
                                   name TEXT NOT NULL PRIMARY KEY,
                                   wins INTEGER NOT NULL DEFAULT 0,
                                   last_win TEXT)
                                '''
                                )
        self.connection.commit()

    def save_win(self, name: str):
        self.connection.execute('''INSERT INTO winners (name, wins, last_win) VALUES (:name, 1, :date)
                                ON CONFLICT(name) DO UPDATE SET
                                wins = wins + 1,
                                last_win = :date''', {'name': name, 'date': datetime.now().isoformat(timespec='seconds')
                                })
        self.connection.commit()

    def get_wins(self, name: str) -> int:
        result = self.connection.execute('SELECT wins FROM winners WHERE name = ?', (name,)).fetchone()
        return result[0] if result else 0
    
    def retrieve_ranking(self) -> list:
        return self.connection.execute('SELECT name, wins from WINNERS ORDER BY wins DESC').fetchall()

    def close(self):
        return self.connection.close()
