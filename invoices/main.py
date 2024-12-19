from invoices.routers import invoices

from fastapi import FastAPI


app = FastAPI()

app.include_router(invoices.router)
