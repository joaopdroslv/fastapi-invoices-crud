from invoices.enums.payment_method import PaymentMethod

from pydantic import BaseModel, Field, model_validator
from datetime import date
from typing import Optional


class InvoiceResponse(BaseModel):
    id: int
    value: float = Field(gt=0)
    paid: bool
    payment_date: Optional[date]
    payment_method: Optional[PaymentMethod]

    # Habilita conversão do model Invoice do ORM para o InvoiceResponse
    class ConfigDict:
        from_attributes = True


class InvoiceRequest(BaseModel):
    value: float
    paid: bool
    payment_date: Optional[date]
    payment_method: Optional[PaymentMethod]

    @model_validator(mode='before')
    def validate_paid_fields(cls, values):
        paid = values.get('paid')

        if not paid:
            values['payment_date'] = None
            values['payment_method'] = None

        return values
