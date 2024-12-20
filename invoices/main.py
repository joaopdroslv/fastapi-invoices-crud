from invoices.routers import invoices_router

from shared.exceptions import NotFound
from shared.exceptions_handlers import not_found_exception_handler

from fastapi import FastAPI


app = FastAPI()


app.add_exception_handler(NotFound, not_found_exception_handler)

app.include_router(invoices_router.router)
