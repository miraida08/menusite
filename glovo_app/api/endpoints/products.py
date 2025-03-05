from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from glovo_app.db.models import Product
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import ProductSchema


product_router = APIRouter(prefix='/product', tags=['Products'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# product
@product_router.post('/product/create/', response_model=ProductSchema)
async def product_create(product: ProductSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get('/product/', response_model=List[ProductSchema])
async def product_list(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get('/product/{product_id}/', response_model=ProductSchema)
async def product_detail(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='product not found')
    return product


@product_router.put('/product/{product_id}/', response_model=ProductSchema)
async def product_update(product_id: int, product_data: ProductSchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='product not found')
    for product_key, product_value in product_data.dict().items():
        setattr(product, product_key, product_value)
    db.commit()
    db.refresh(product)
    return product


@product_router.delete('/product/{product_id}/')
async def product_delete(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='product not found')
    db.delete(product)
    db.commit()
    return {'message': 'this product is deleted'}