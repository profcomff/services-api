from .base import Base


class ScopeCreate(Base):
    name: str


class ScopeGet(Base):
    id: int
    name: str
