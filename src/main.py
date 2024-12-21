from src.routers import invoices_router, users_router

from src.exceptions import NotFound
from src.exceptions_handlers import not_found_exception_handler

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API is running"}


app.add_exception_handler(NotFound, not_found_exception_handler)

app.include_router(invoices_router.router)
app.include_router(users_router.router)
