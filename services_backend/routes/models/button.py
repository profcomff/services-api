from .base import Base


class ButtonCreate(Base):
    icon: str
    name: str
    link: str
    type: str


class ButtonUpdate(Base):
    category_id: int | None
    icon: str | None
    name: str | None
    order: int | None
    link: str | None
    type: str | None


class ButtonGet(Base):
    id: int
    order: int
    icon: str | None
    name: str | None
    link: str | None
    type: str | None
