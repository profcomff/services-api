from pydantic import BaseModel


class CategoryBase(BaseModel):
    id: int
    category_id: int


class CategoryCreate(CategoryBase):
    type: str
    name: str


class CategoryDelete(CategoryBase):
    type: str
    name: str


class Category(CategoryBase):
    type: str
    name: str

    class Config:
        orm_mode = True


class ButtonBase(BaseModel):
    id: int
    category_id: int


class ButtonCreate(ButtonBase):
    name: str
    icon: str


class ButtonDelete(ButtonBase):
    name: str
    icon: str


class Button(ButtonBase):
    name: str
    icon: str

    class Config:
        orm_mode = True
