import sqlite3
from datetime import datetime
from datetime import timedelta

from Borrower import Borrower
from Loan import Loan


class DbConnection:
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self, database_file: str):
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Blacklist (Personal_id INTEGER PRIMARY KEY)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Loans (ID INTEGER PRIMARY KEY AUTOINCREMENT, Amount INTEGER, 
        TERM INTEGER, Name TEXT, Borrower_id INTEGER, Loan_time timestamp)''')

    def is_blacklisted(self, borrower_id: int) -> bool:
        results = self.cursor.execute("SELECT * from Blacklist WHERE Personal_id = ?", [borrower_id])
        if results.fetchone() is not None:
            return True
        return False

    def too_many_applications(self, personal_id: int) -> bool:
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        params = (personal_id, yesterday, now)
        self.cursor.execute("SELECT * FROM Loans WHERE Borrower_id = ? AND Loan_time BETWEEN ? AND ?",
                            params)
        count = len(self.cursor.fetchall())
        if count > 1:
            return True
        return False

    def add_loan(self, amount: int, term: int, name: str, borrower_id: int):
        params = (amount, term, name, borrower_id, datetime.now())
        self.cursor.execute("INSERT INTO Loans (amount, term, name, borrower_id, loan_time) VALUES (?, "
                            "?, ?, ?, ?)", params)
        self.conn.commit()

    def list_loans(self, borrower_id):
        self.cursor.execute("SELECT * from Loans WHERE Borrower_id = ?", [borrower_id])
        results = self.cursor.fetchall()
        loans = []
        for loan in results:
            loans.append(Loan(amount=loan[1], term=loan[2], borrower=Borrower(name=loan[3], personal_id=loan[4])))

        return {"Loans": loans}
