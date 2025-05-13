import sqlite3

conn = sqlite3.connect('jobs.db')

c = conn.cursor()

c.execute('''
    CREATE TABLE jobs (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          company TEXT NOT NULL,
          link TEXT,
          date TEXT
          )
''')

conn.commit()
conn.close()

print("DB created")