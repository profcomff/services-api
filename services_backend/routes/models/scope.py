from .base import Base


class ScopeCreate(Base):
    name: str
    category_id: int | None


class ScopeGet(Base):
    id: int
    name: str


class ScopeUpdate(Base):
    name: str | None
    category_id: int | None
