from .base import Base


class CategoryCreate(Base):
    type: str | None
    name: str | None


class CategoryUpdate(Base):
    type: str | None
    name: str | None


class CategoryGet(Base):
    id: int
    type: str | None
    name: str | None

