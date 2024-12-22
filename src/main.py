from src.routers import invoices_router, users_router
from src.exceptions import (
    NotFound, 
    InvoiceAlready, 
    InvalidPaymentMethod
)
from src.exceptions_handlers import (
    not_found_exception_handler, 
    invoice_already_exception_handler, 
    invalid_payment_method_exception_handler
)

from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is running"}

app.add_exception_handler(NotFound, not_found_exception_handler)
app.add_exception_handler(InvoiceAlready, invoice_already_exception_handler)
app.add_exception_handler(InvalidPaymentMethod, invalid_payment_method_exception_handler)

app.include_router(invoices_router.router)
app.include_router(users_router.router)
