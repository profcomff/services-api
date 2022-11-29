from fastapi import FastAPI

from ..settings import Settings
from .button import button
from .category import category
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

# Насрано вот тут
settings = Settings()
app = FastAPI(debug=True)
app.include_router(button)
app.include_router(category)


app.add_middleware(
    DBSessionMiddleware,
    db_url=settings.DB_DSN,
    session_args={"autocommit": True},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
