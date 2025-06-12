from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.exceptions import InvalidPaymentMethod, InvoiceAlready, NotFound
from app.models.invoice_model import Invoice
from app.schemas.invoice_schema import (
    BasicInvoiceRequest,
    PaymentInfoRequest,
    PaymentMethod,
)
from app.service.user_service import find_user_by_id


def find_invoice_by_id(invoice_id: int, db: Session) -> Invoice:
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise NotFound("Invoice")
    return invoice


def set_invoice_as_paid(
    invoice_id: int, payment_info: PaymentInfoRequest, db: Session
) -> Invoice:
    db_invoice = find_invoice_by_id(invoice_id, db)

    if payment_info.payment_method not in PaymentMethod.__members__:
        raise InvalidPaymentMethod(payment_info.payment_method)

    if db_invoice.paid:
        raise InvoiceAlready(invoice_id, "paid")

    db_invoice.paid = True
    db_invoice.paid_value = payment_info.paid_value

    if db_invoice.remaining_value < 0:
        # Change this to a custom exception
        raise HTTPException(
            status_code=422, detail="You cannot pay more than the invoice total."
        )

    db_invoice.payment_date = datetime.now()
    db_invoice.payment_method = PaymentMethod[payment_info.payment_method]

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def link_invoice_to_an_user(
    db_invoice: Invoice, provided_invoice: BasicInvoiceRequest, db: Session
):
    db_user = find_user_by_id(provided_invoice.user_id, db)

    if db_invoice.user_id:
        raise InvoiceAlready(db_invoice.id, "linked to an user")

    if not db_invoice.user_id:
        db_invoice.user_id = db_user.id
