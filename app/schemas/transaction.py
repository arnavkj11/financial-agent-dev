from pydantic import BaseModel, Field
from typing import List, Optional

class Transaction(BaseModel):
    date: str = Field(description="The date of the transaction in YYYY-MM-DD format")
    merchant: str = Field(description="The name of the merchant or description of transaction")
    amount: float = Field(description="The absolute amount of the transaction")
    currency: str = Field(description="Currency code, e.g., USD, EUR", default="USD")
    category: Optional[str] = Field(description="Inferred category e.g., Food, Transport, Utilities", default=None)

class ExtractedFinancialData(BaseModel):
    transactions: List[Transaction]
    summary: str = Field(description="Brief summary of the statement period and total spend")
