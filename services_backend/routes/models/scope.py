from .base import Base


class ScopeCreate(Base):
    read_scope: str | None


class ScopeGet(Base):
    id: int
    read_scope: str


class ScopeUpdate(Base):
    read_scope: str | None
