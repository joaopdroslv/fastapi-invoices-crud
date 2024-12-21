from src.exceptions import NotFound
from src.models.invoice_model import Invoice

from sqlalchemy.orm import Session


def find_invoice_by_id(invoice_id: int, db: Session) -> Invoice:
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise NotFound('Invoice')
    return invoice
