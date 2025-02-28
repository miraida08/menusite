from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from glovo_app.db.models import ProductCombo
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import ProductComboSchema


product_combo_router = APIRouter(prefix='/auth', tags=['Auth'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# product_combo
@product_combo_router.post('/product_combo/create/', response_model=ProductComboSchema)
async def product_combo_create(product_combo: ProductComboSchema, db: Session = Depends(get_db)):
    product_combo_db = ProductCombo(**product_combo.dict())
    db.add(product_combo_db)
    db.commit()
    db.refresh(product_combo_db)
    return product_combo_db


@product_combo_router.get('/product_combo/', response_model=List[ProductComboSchema])
async def product_combo_list(db: Session = Depends(get_db)):
    return db.query(ProductCombo).all()


@product_combo_router.get('/product_combo/{product_combo_id}/', response_model=ProductComboSchema)
async def product_combo_detail(product_combo_id: int, db: Session = Depends(get_db)):
    product_combo = db.query(ProductCombo).filter(ProductCombo.id == product_combo_id).first()
    if product_combo is None:
        raise HTTPException(status_code=404, detail='product_combo not found')
    return product_combo


@product_combo_router.put('/product_combo/{product_combo_id}/', response_model=ProductComboSchema)
async def product_combo_update(product_combo_id: int, product_combo_data: ProductComboSchema, db: Session = Depends(get_db)):
    product_combo = db.query(ProductCombo).filter(ProductCombo.id == product_combo_id).first()
    if product_combo is None:
        raise HTTPException(status_code=404, detail='product_combo not found')
    for product_combo_key, product_combo_value in product_combo_data.dict().items():
        setattr(product_combo, product_combo_key, product_combo_value)
    db.commit()
    db.refresh(product_combo)
    return product_combo


@product_combo_router.delete('/product_combo/{product_combo_id}/')
async def product_combo_delete(product_combo_id: int, db: Session = Depends(get_db)):
    product_combo = db.query(ProductCombo).filter(ProductCombo.id == product_combo_id).first()
    if product_combo is None:
        raise HTTPException(status_code=404, detail='product_combo not found')
    db.delete(product_combo)
    db.commit()
    return {'message': 'this product_combo is deleted'}