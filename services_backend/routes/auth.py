from auth_lib.fastapi import UnionAuth
from services_backend.settings import get_settings

settings = get_settings()

auth = UnionAuth(settings.AUTH_URL)