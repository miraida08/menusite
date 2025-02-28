from pydantic import BaseModel
from glovo_app.db.models import *


class UserProfileSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    phone_number: Optional[str] = None
    role: UserRole


class CategorySchema(BaseModel):
    id: int
    category_name: str


class StoreSchema(BaseModel):
    id: int
    store_name: str
    store_description: str
    address: str
    store_image: str
    owner_id: int
    category_id: int


class ContactSchema(BaseModel):
    id: int
    phone_number: Optional[str] = None
    store_id: int


class ProductSchema(BaseModel):
    id: int
    product_name: str
    product_description: str
    price: int
    product_image: str
    store_id: int


class ProductComboSchema(BaseModel):
    id: int
    product_name: str
    description: str
    price: int
    image: str
    store_id: int


class OrderSchema(BaseModel):
    id: int
    delivery_address: str
    created_date: datetime
    role: OrderRole
    client_id: int
    courier_id: int


class CourierSchema(BaseModel):
    user_id: int
    role: CourierRole
    order_id: int


class StoreReviewSchema(BaseModel):
    store_id: int
    client_id: int
    created_date: datetime
    comment: str
    rating: ReviewChoices


class CourierReviewSchema(BaseModel):
    courier_id: int
    client_id: int
    created_date: datetime
    comment: str
    rating: ReviewChoices
















