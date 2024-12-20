from invoices.routers import invoices_router, users_router

from shared.exceptions import NotFound
from shared.exceptions_handlers import not_found_exception_handler

from fastapi import FastAPI
import uvicorn


app = FastAPI()

app.add_exception_handler(NotFound, not_found_exception_handler)

app.include_router(invoices_router.router)
app.include_router(users_router.router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
