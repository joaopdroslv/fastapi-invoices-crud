from fastapi import FastAPI

from app.exceptions import InvalidPaymentMethod, InvoiceAlready, NotFound
from app.exceptions_handlers import (
    invalid_payment_method_exception_handler,
    invoice_already_exception_handler,
    not_found_exception_handler,
)
from app.routers import invoices_router, users_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API is running"}


app.add_exception_handler(NotFound, not_found_exception_handler)
app.add_exception_handler(InvoiceAlready, invoice_already_exception_handler)
app.add_exception_handler(
    InvalidPaymentMethod, invalid_payment_method_exception_handler
)

app.include_router(invoices_router.router)
app.include_router(users_router.router)
