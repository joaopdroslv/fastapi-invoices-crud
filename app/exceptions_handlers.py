from app.exceptions import (
    NotFound, 
    InvoiceAlready, 
    InvalidPaymentMethod
)

from fastapi import Request
from fastapi.responses import JSONResponse


async def not_found_exception_handler(request: Request, exception: NotFound):
    return JSONResponse(
        status_code=404,
        content={'message': f'{exception.name} not found.'}
    )


async def invoice_already_exception_handler(request: Request, exception: InvoiceAlready):
    return JSONResponse(
        status_code=422,
        content={'message': f"Invoice ID '{exception.invoice_id}' is already {exception.already}."}
    )


async def invalid_payment_method_exception_handler(request: Request, exception: InvalidPaymentMethod):
    return JSONResponse(
        status_code=422,
        content={'message': f"Payment method '{exception.method}' is invalid."}
    )
