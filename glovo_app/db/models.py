from sqlalchemy import Integer, String, ForeignKey, DateTime, Text, DECIMAL, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List
from glovo_app.db.database import Base
from enum import Enum as PyEnum
from passlib.hash import bcrypt


class UserRole(str, PyEnum):
    courier = 'courier'
    client = 'client'
    owner = 'owner'


class CourierRole(str, PyEnum):
    courier1 = 'доступен'
    courier2 = 'занят'


class OrderRole(str, PyEnum):
    type1 = 'ожидает обработки'
    type2 = 'в процессе доставки'
    type3 = 'доставлен'
    type4 = 'отменен'


class ReviewChoices(str, PyEnum):
    review1 = '1'
    review2 = '2'
    review3 = '3'
    review4 = '4'
    review5 = '5'


class Category(Base):
    __tablename__ = "Category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    category_course: Mapped[List['Store']] = relationship(back_populates='category',
                                                          cascade='all, delete-orphan')


class UserProfile(Base):
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str] = mapped_column(String(40))
    username: Mapped[str] = mapped_column(String(40), unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.client)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    owner_store: Mapped[List["Store"]] = relationship(back_populates="owner",
                                                      cascade='all, delete-orphan')
    client_order: Mapped[List['Order']] = relationship(back_populates='client',
                                                       cascade='all, delete-orphan')
    courier_order: Mapped[List['Order']] = relationship(back_populates='courier',
                                                        cascade='all, delete-orphan')
    user_courier: Mapped[List['Courier']] = relationship(back_populates='user',
                                                         cascade='all, delete-orphan')
    client_review: Mapped[List['Courier']] = relationship(back_populates='client',
                                                          cascade='all, delete-orphan')
    courier_review: Mapped[List['CourierReview']] = relationship(back_populates='courier',
                                                                 cascade='all, delete-orphan')
    client_courier: Mapped[List['CourierReview']] = relationship(back_populates='client',
                                                                 cascade='all, delete-orphan')
    tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                        cascade='all, delete-orphan')

    # register
    def set_password(self, password: str):
        self.hashed_password = bcrypt.hash(password)

    # login
    def check_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')


class Store(Base):
    __tablename__ = "Store"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    store_name: Mapped[str] = mapped_column(String(40))
    store_description: Mapped[str] = mapped_column(Text)
    address: Mapped[str] = mapped_column(String)
    store_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    owner: Mapped["UserProfile"] = relationship("UserProfile", back_populates="owner_store")

    category_id: Mapped[int] = mapped_column(ForeignKey('Category.id'))
    category: Mapped['Category'] = relationship(back_populates='category_course')

    contact_store: Mapped[List['Contact']] = relationship(back_populates='store',
                                                          cascade='all, delete-orphan')
    product_store: Mapped[List['Product']] = relationship(back_populates='store',
                                                          cascade='all, delete-orphan')
    product_combo: Mapped[List['ProductCombo']] = relationship(back_populates='store',
                                                               cascade='all, delete-orphan')
    store_review: Mapped[List['ProductCombo']] = relationship(back_populates='store',
                                                              cascade='all, delete-orphan')


class Contact(Base):
    __tablename__ = "Contact"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    store_id: Mapped[int] = mapped_column(ForeignKey('Store.id'))
    store: Mapped['Store'] = relationship(back_populates='contact_store')


class Product(Base):
    __tablename__ = "Product"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    product_name: Mapped[str] = mapped_column(String(40))
    product_description: Mapped[str] = mapped_column(Text)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(8, 2))
    product_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    store_id: Mapped[int] = mapped_column(ForeignKey('Store.id'))
    store: Mapped['Store'] = relationship(back_populates='product_store')


class ProductCombo(Base):
    __tablename__ = "ProductCombo"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    product_name: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(8, 2))
    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    store_id: Mapped[int] = mapped_column(ForeignKey('Store.id'))
    store: Mapped['Store'] = relationship(back_populates='product_combo')


class Order(Base):
    __tablename__ = "Order"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    delivery_address: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    role: Mapped[OrderRole] = mapped_column(Enum(OrderRole), nullable=False, default=OrderRole.type1)

    client_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    client: Mapped["UserProfile"] = relationship("UserProfile", back_populates="client_order")

    courier_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    courier: Mapped["UserProfile"] = relationship("UserProfile", back_populates="courier_order")

    order_courier: Mapped[List['Courier']] = relationship(back_populates='order',
                                                          cascade='all, delete-orphan')


class Courier(Base):
    __tablename__ = "Courier"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    user: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user_courier")

    role: Mapped[CourierRole] = mapped_column(Enum(CourierRole), nullable=False, default=CourierRole.courier1)
    order_id: Mapped[int] = mapped_column(ForeignKey("Order.id"))

    order: Mapped["Order"] = relationship("Order", back_populates="order_courier")


class StoreReview(Base):
    __tablename__ = "StoreReview"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('Store.id'))
    store: Mapped['Store'] = relationship(back_populates='store_review')

    client_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    client: Mapped["UserProfile"] = relationship("UserProfile", back_populates="client_review")

    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    comment: Mapped[str] = mapped_column(Text)
    rating: Mapped[ReviewChoices] = mapped_column(Enum(ReviewChoices), nullable=False, default=ReviewChoices.review1)


class CourierReview(Base):
    __tablename__ = "CourierReview"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    courier_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    courier: Mapped["UserProfile"] = relationship("UserProfile", back_populates="courier_review")

    client_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    client: Mapped["UserProfile"] = relationship("UserProfile", back_populates="client_courier")

    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    rating: Mapped[ReviewChoices] = mapped_column(Enum(ReviewChoices), nullable=False, default=ReviewChoices.review1)












