from .base import Base


class ButtonCreate(Base):
    category_id: int
    icon: str | None
    name: str | None
    link: dict | None

class ButtonUpdate(Base):
    category_id: int | None
    icon: str | None
    name: str | None
<<<<<<< Updated upstream
=======
    order: int | None
    link: dict | None
>>>>>>> Stashed changes


class ButtonGet(Base):
    id: int
    category_id: int
    icon: str | None
    name: str | None
    link: dict | None
