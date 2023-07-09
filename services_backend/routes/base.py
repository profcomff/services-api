from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from services_backend import __version__
from services_backend.settings import get_settings

from .button import button
from .category import category


# from .scope import scope


settings = get_settings()
app = FastAPI(
    title='API управления списком сервисов',
    description='Программный интерфейс управления списком сервисов в приложении Твой ФФ!',
    version=__version__,
    # Настраиваем интернет документацию
    root_path=settings.ROOT_PATH if __version__ != 'dev' else '/',
    docs_url=None if __version__ != 'dev' else '/docs',
    redoc_url=None,
)


app.add_middleware(
    DBSessionMiddleware,
    db_url=str(settings.DB_DSN),
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(button, prefix='/category/{category_id}/button', tags=["Button"])
app.include_router(category, prefix='/category', tags=["Category"])
