import sqlite3

conn = sqlite3.connect('jobs.db')

c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          company TEXT NOT NULL,
          link TEXT,
          date DATE,
          FOREIGN KEY (user_id) REFERENCES users(id) 
          )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT UNIQUE NOT NULL,
          password TEXT NOT NULL
          )
''')

conn.commit()
conn.close()

print("DB created")