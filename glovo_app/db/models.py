from sqlalchemy import Integer, String, ForeignKey, DateTime, Text, DECIMAL, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List
from glovo_app.db.database import Base
from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    client = 'клиент'
    cour = 'курьер'
    owner = 'владелец'


class OrderStatus(str, PyEnum):
    tim1 = 'Ожидает обработки'
    tim2 = 'В процессе доставки'
    tim3 = 'Доставлкн'
    tim4 = 'Отменен'


class CourierStatus(str, PyEnum):
    cour1 = 'доступен'
    cour2 = 'занят'


class RatingStatus(str, PyEnum):
    rating1 = '1'
    rating2 = '2'
    rating3 = '3'
    rating4 = '4'
    rating5 = '5'



class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(40))
    last_name: Mapped[str] = mapped_column(String(40))
    username: Mapped[str] = mapped_column(String(40), unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates='user',
                                                        cascade='all, delete')

    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.client.value)
    store: Mapped[List["Store"]] = relationship("Store", back_populates='user',
                                                        cascade='all, delete')
    # client: Mapped[List["Order"]] = relationship("Order", back_populates="clients_order",
    #                                              cascade="all, delete")
    # courier: Mapped[List["Order"]] = relationship("Order", back_populates="courier_order",
    #                                               cascade="all, delete")
    courier_user: Mapped[List["Courier"]] = relationship("Courier", back_populates='couriers',
                                                        cascade='all, delete')
    clients: Mapped[List["StoreReview"]] = relationship("StoreReview", back_populates='client',
                                                        cascade='all, delete')
    # client_review: Mapped[List["CourierReview"]] = relationship("CourierReview",
    #                                                             back_populates="clients_review",
    #                                                             cascade="all, delete")
    # courier_review: Mapped[List["CourierReview"]] = relationship("CourierReview",
    #                                                              back_populates="couriers_review",
    #                                                              cascade="all, delete")


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='tokens')



class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_name: Mapped[str] = mapped_column(String(55))
    category: Mapped[List["Store"]] = relationship("Store", back_populates='category_store',
                                                    cascade='all, delete')


class Store(Base):
    __tablename__ = "store"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    store_name: Mapped[str] = mapped_column(String(55), index=True)
    store_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text)
    address: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='store')
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category_store: Mapped['Category'] = relationship('Category', back_populates='category')
    contact_store: Mapped[List["ContactInfo"]] = relationship("ContactInfo", back_populates='contact_infos',
                                                   cascade='all, delete')
    product: Mapped[List["Product"]] = relationship("Product", back_populates='product_store',
                                                   cascade='all, delete')
    product_combo: Mapped[List["ProductCombo"]] = relationship("ProductCombo", back_populates='product_store',
                                                               cascade='all, delete')
    store: Mapped[List["StoreReview"]] = relationship("StoreReview", back_populates='store_reviews',
                                                      cascade='all, delete')

class ContactInfo(Base):
    __tablename__ = "contact_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    contact_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    contact_infos: Mapped['Store'] = relationship('Store', back_populates='contact_store')


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_name: Mapped[str] = mapped_column(String(55), index=True)
    product_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(8, 2))
    description: Mapped[str] = mapped_column(Text)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    product_store: Mapped['Store'] = relationship('Store', back_populates='product')


class ProductCombo(Base):
    __tablename__ = "product_combo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    combo_name: Mapped[str] = mapped_column(String(55), index=True)
    combo_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(8, 2))
    description: Mapped[str] = mapped_column(Text)
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    product_store: Mapped['Store'] = relationship('Store', back_populates='product_combo')



class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.tim1.value)
    delivery_address: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # client_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    # clients: Mapped['UserProfile'] = relationship('UserProfile', back_populates='client')
    # courier_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    # courier: Mapped['UserProfile'] = relationship('UserProfile', back_populates='courier')


class Courier(Base):
    __tablename__ = "couriers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    status_courier: Mapped[CourierStatus] = mapped_column(Enum(CourierStatus), nullable=False,
                                                          default=CourierStatus.cour1.value)
    courier_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    couriers: Mapped['UserProfile'] = relationship('UserProfile', back_populates='courier_user')


class StoreReview(Base):
    __tablename__ = "store_review"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rating: Mapped[RatingStatus] = mapped_column(Enum(RatingStatus), nullable=False, default=RatingStatus.rating5.value)
    commend: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    client_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    client = relationship("UserProfile", back_populates="clients")
    store_id: Mapped[int] = mapped_column(ForeignKey('store.id'))
    store_reviews: Mapped['Store'] = relationship('Store', back_populates='store')


class CourierReview(Base):
    __tablename__ = "courier_review"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # client_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))
    # client = relationship("UserProfile", back_populates="client_review")
    # courier_id: Mapped[int] = mapped_column(ForeignKey('user_profiles.id'))
    # courier: Mapped['UserProfile'] = relationship('UserProfile', back_populates='courier_review')
    rating: Mapped[RatingStatus] = mapped_column(Enum(RatingStatus), nullable=False, default=RatingStatus.rating5.value)
    commend: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)