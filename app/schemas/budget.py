from pydantic import BaseModel

class BudgetCreate(BaseModel):
    category: str
    amount: float

class BudgetOut(BaseModel):
    id: int
    category: str
    amount: float

    class Config:
        from_attributes = True

class BudgetStatus(BaseModel):
    category: str
    limit: float
    spent: float
    remaining: float
    percent_used: float
