import sqlite3

conn = sqlite3.connect("loandatabase.db")
cursor = conn.cursor()

cursor.execute("""
    DROP TABLE Loans
""")

cursor.execute("""
    DROP TABLE Blacklist
""")




