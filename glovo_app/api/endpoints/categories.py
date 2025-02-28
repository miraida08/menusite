from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from glovo_app.db.models import Category
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import CategorySchema


category_router = APIRouter(prefix='/auth', tags=['Auth'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#category
@category_router.post('category/create/', response_model=CategorySchema)
async def create_category(category: CategorySchema, db: Session = Depends(get_db)):
    db_category = Category(category_name=category.category_name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@category_router.get('/category/', response_model=List[CategorySchema])
async def list_category(db: Session = Depends(get_db)):
    return db.query(Category).all()


@category_router.put('/category/{category_id', response_model=CategorySchema)
async def update_category(category_id: int,
                          category_data: CategorySchema,
                          db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category not found')
    category.category_name = category_data.category_name
    db.commit()
    db.refresh(category)
    return category


@category_router.delete('/category/{category_id', response_model=CategorySchema)
async def update_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail='Category not found')
    db.delete(category)
    db.commit()
    return category