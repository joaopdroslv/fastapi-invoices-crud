from app.database.dependencies import get_db
from app.models.invoice_model import Invoice
from app.schemas.invoice_schema import (
    BasicInvoiceRequest,  
    PaymentInfoRequest, 
    InvoiceResponse
)
from app.service.invoice_service import (
    find_invoice_by_id, 
    set_invoice_as_paid, 
    link_invoice_to_an_user
)
from app.service.user_service import find_user_by_id

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix='/invoices')


@router.get('/', response_model=List[InvoiceResponse], status_code=200)
def list_invoices(db: Session = Depends(get_db)) -> List[InvoiceResponse]:
    return db.query(Invoice).all()


@router.get('/{invoice_id}', response_model=InvoiceResponse, status_code=200)
def list_invoice(invoice_id: int , db: Session = Depends(get_db)) -> InvoiceResponse:
    return find_invoice_by_id(invoice_id, db)


@router.post('/', response_model=InvoiceResponse, status_code=201)
def create_invoice(provided_invoice: BasicInvoiceRequest, db: Session = Depends(get_db)) -> InvoiceResponse:
    if provided_invoice.user_id:
        # If the provided user id is invalid this will raise NotFound (404) error
        find_user_by_id(provided_invoice.user_id, db)

    db_invoice = Invoice(**provided_invoice.model_dump())

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


@router.put('/{invoice_id}/pay', response_model=InvoiceResponse, status_code=200)
def pay_invoice(invoice_id: int, provided_invoice: PaymentInfoRequest, db: Session = Depends(get_db)) -> InvoiceResponse:
    db_invoice = set_invoice_as_paid(invoice_id, provided_invoice, db)
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


@router.put('/{invoice_id}', response_model=InvoiceResponse, status_code=200)
def update_invoice(invoice_id: int, provided_invoice: BasicInvoiceRequest, db: Session = Depends(get_db)) -> InvoiceResponse:
    db_invoice = find_invoice_by_id(invoice_id, db)

    if provided_invoice.user_id:
        link_invoice_to_an_user(db_invoice, provided_invoice, db)

    db_invoice.value = provided_invoice.value

    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


@router.delete('/{invoice_id}', status_code=204)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)) -> None:
    db_invoice = find_invoice_by_id(invoice_id, db)
    db.delete(db_invoice)
    db.commit()
