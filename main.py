from fastapi import FastAPI

from Loan import Loan
from db_connection import DbConnection

app = FastAPI()
connection = DbConnection("loandatabase.db")


@app.get("/")
async def root():
    return "AdCash Loan Application"


@app.post("/apply")
async def apply_for_loan(loan: Loan) -> str:
    personal_id = loan.borrower.personal_id
    amount = loan.amount
    term = loan.term
    name = loan.borrower.name

    if connection.is_blacklisted(personal_id):
        return "Application rejected. Applicant is blacklisted"
    if connection.too_many_applications(personal_id):
        return "Application rejected. Too many applications in the last 24 hours."

    connection.add_loan(amount, term, name, personal_id)

    return f"Monthly payment for loan: {loan.to_string()} - " + str(loan.monthly_payment())


@app.get("/loans/{borrower_id}")
async def loans_by_borrower(borrower_id):
    loans = connection.list_loans(borrower_id)
    return loans
