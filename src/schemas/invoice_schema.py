from src.schemas.user_schema import UserResponse

from pydantic import BaseModel, Field, model_validator
from datetime import date
from enum import Enum
from typing import Optional


class PaymentMethod(str, Enum):
    cash = 'cash'
    credit_card = 'credit_card'
    debit_card = 'debit_card'


class InvoiceResponse(BaseModel):
    id: int
    value: float
    paid: bool
    payment_date: Optional[date]
    payment_method: Optional[PaymentMethod]
    user: Optional[UserResponse] = None

    class ConfigDict:
        from_attributes = True


class InvoiceRequest(BaseModel):
    value: float = Field(gt=0)
    paid: bool
    payment_date: Optional[date] = None
    payment_method: Optional[PaymentMethod] = None
    user_id: Optional[int] = None

    @model_validator(mode='before')
    def validate_paid_fields(cls, values):
        paid = values.get('paid')
        payment_date = values.get('payment_date')
        payment_method = values.get('payment_method')

        if not paid:
            values['payment_date'] = None
            values['payment_method'] = None
        elif paid:
            if payment_date is None:
                raise ValueError('Payment date must be provided when paid is True.')
            if payment_method is None:
                raise ValueError('Payment method must be provided when paid is True.')

        return values
