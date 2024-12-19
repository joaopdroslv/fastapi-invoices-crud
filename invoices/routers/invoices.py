from shared.dependencies import get_db

from invoices.models.invoice import Invoice
from invoices.schemas.invoice import InvoiceRequest, InvoiceResponse

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix='/invoices')


@router.get('/', response_model=List[InvoiceResponse], status_code=200)
def list_invoices(db: Session = Depends(get_db)) -> List[InvoiceResponse]:
    invoices = db.query(Invoice).all()
    return invoices


@router.get('/{id}', response_model=InvoiceResponse, status_code=200)
def list_invoice(id:int , db: Session = Depends(get_db)) -> InvoiceResponse:
    invoice = db.query(Invoice).filter(Invoice.id == id).first()
    return invoice


@router.post('/', response_model=InvoiceResponse, status_code=201)
def create_invoice(provided_invoice: InvoiceRequest, db: Session = Depends(get_db)) -> InvoiceResponse:
    new_invoice = Invoice(**provided_invoice.model_dump())  # Parametros nomeados

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    # Retornando o InvoiceResponse, convertendo automático a partir do model Invoice do ORM
    return new_invoice


@router.put('/{id}', response_model=InvoiceResponse, status_code=200)
def update_invoice(id: int, provided_invoice: InvoiceRequest, db: Session = Depends(get_db)) -> InvoiceResponse:
    invoice: Invoice = db.query(Invoice).filter(Invoice.id == id).first()

    invoice.value = provided_invoice.value
    invoice.paid = provided_invoice.paid  
    invoice.payment_date = provided_invoice.payment_date
    invoice.payment_method = provided_invoice.payment_method

    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    # Retornando o InvoiceResponse, convertendo automático a partir do model Invoice do ORM
    return invoice


@router.delete('/{id}', status_code=204)
def delete_invoice(id: int, db: Session = Depends(get_db)) -> None:
    invoice = db.query(Invoice).filter(Invoice.id == id).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(invoice)
    db.commit()
