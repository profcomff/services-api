import pytest
import json
from starlette import status
from services_backend.settings import get_settings


class TestCategory:
    _url = '/category/'
    settings = get_settings()

