from fastapi import FastAPI
import logging
from api.views import router

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    redoc_url=None,
    docs_url = "/",
    description=(
        "**Todo list panel backend APIs**\n\n"
        "Use these endpoints to create, list, update, and delete tasks."
    ),
)

# Include your API routes
app.include_router(router)

