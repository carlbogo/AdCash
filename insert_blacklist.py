import sqlite3

conn = sqlite3.connect("loandatabase.db")
cursor = conn.cursor()

cursor.execute('''INSERT INTO Blacklist (Personal_id) VALUES (?)''', [29])
conn.commit()
