from .base import Base


class ButtonCreate(Base):
    category_id: int
    order: int
    icon: str | None
    name: str | None


class ButtonUpdate(Base):
    category_id: int | None
    icon: str | None
    name: str | None
    order: int | None


class ButtonGet(Base):
    id: int
    category_id: int
    order: int | None
    icon: str | None
    name: str | None
