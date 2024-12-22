from src.schemas.user_schema import UserResponse

from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum
from typing import Optional


class PaymentMethod(str, Enum):
    cash = 'Cash'
    credit_card = 'Credit Card'
    debit_card = 'Debit Card'


class InvoiceResponse(BaseModel):
    id: int

    value: float
    paid_value: float
    remaining_value: float
    paid: bool
    full_payment: bool
    payment_date: Optional[datetime] = None
    payment_method: Optional[PaymentMethod] = None

    user: Optional[UserResponse] = None

    class ConfigDict:
        from_attributes = True


class BasicInvoiceRequest(BaseModel):
    value: float = Field(gt=0)
    user_id: Optional[int] = None


class PaymentInfoRequest(BaseModel):
    paid_value: float = Field(gt=0)
    payment_method: str
