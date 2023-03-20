from pydantic import BaseModel
from Borrower import Borrower


class Loan(BaseModel):
    amount: int  # base amount
    term: int  # in years
    borrower: Borrower

    def monthly_payment(self):
        future_value = self.amount * 1.05 ** (self.term * 12)
        monthly_payment = round(future_value / (self.term * 12), 2)
        return str(monthly_payment)

    def to_string(self):
        return f"[Amount: {self.amount}, term: {self.term} for borrower {self.borrower.name} with Personal ID: {self.borrower.personal_id}] "
