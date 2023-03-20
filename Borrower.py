from pydantic import BaseModel


class Borrower(BaseModel):
    name: str
    personal_id: int
