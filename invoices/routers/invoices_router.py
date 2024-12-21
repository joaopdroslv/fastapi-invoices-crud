from shared.dependencies import get_db
from invoices.models.invoice_model import Invoice
from invoices.schemas.invoice_schema import InvoiceRequest, InvoiceResponse
from invoices.crud.invoice_crud import find_invoice_by_id
from invoices.crud.user_crud import find_user_by_id

from fastapi import APIRouter, Depends, HTTPException
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
def create_invoice(provided_invoice: InvoiceRequest, db: Session = Depends(get_db)) -> InvoiceResponse:
    if provided_invoice.user_id:
        # If the provided user id is invalid this will raise NotFound (404) error
        find_user_by_id(provided_invoice.user_id, db)

    new_invoice = Invoice(**provided_invoice.model_dump())

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice


@router.put('/{invoice_id}', response_model=InvoiceResponse, status_code=200)
def update_invoice(invoice_id: int, provided_invoice: InvoiceRequest, db: Session = Depends(get_db)) -> InvoiceResponse:
    invoice = find_invoice_by_id(invoice_id, db)

    invoice.value = provided_invoice.value
    invoice.paid = provided_invoice.paid  
    invoice.payment_date = provided_invoice.payment_date
    invoice.payment_method = provided_invoice.payment_method

    # Once linked to an user, you can no longer update the invoice user 
    if invoice.user_id and provided_invoice.user_id:
        raise HTTPException(status_code=422, detail="Cannot change the user to witch the invoice is linked")

    if not invoice.user_id and provided_invoice.user_id:
        # If the provided user id is invalid this will raise NotFound (404) error
        find_user_by_id(provided_invoice.user_id, db)  
        invoice.user_id = provided_invoice.user_id

    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@router.delete('/{invoice_id}', status_code=204)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)) -> None:
    invoice = find_invoice_by_id(invoice_id, db)
    db.delete(invoice)
    db.commit()
