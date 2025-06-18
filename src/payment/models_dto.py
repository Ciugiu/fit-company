from pydantic import BaseModel, Field
from typing import List, Optional

class UserSchema(BaseModel):
    email: str
    name: str

class PaymentSchema(BaseModel):
    id: int
    user_email: str
    amount: float
    currency: str
    status: str
    created_at: str

class PaymentResponseSchema(BaseModel):
    payment: PaymentSchema
    message: str

class PaymentHistorySchema(BaseModel):
    user_email: str
    payments: List[PaymentSchema] = Field(default_factory=list)