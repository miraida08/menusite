from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from glovo_app.db.models import Store
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import StoreSchema


stores_router = APIRouter(prefix='/auth', tags=['Auth'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# store
@stores_router.post('/store/create/', response_model=StoreSchema)
async def store_create(store: StoreSchema, db: Session = Depends(get_db)):
    store_db = Store(**store.dict())
    db.add(store_db)
    db.commit()
    db.refresh(store_db)
    return store_db


@stores_router.get('/store/', response_model=List[StoreSchema])
async def store_list(db: Session = Depends(get_db)):
    return db.query(Store).all()


@stores_router.get('/store/{store_id}/', response_model=StoreSchema)
async def store_detail(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail='store not found')
    return store


@stores_router.put('/store/{store_id}/', response_model=StoreSchema)
async def store_update(store_id: int, store_data: StoreSchema, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail='Course not found')
    for store_key, store_value in store_data.dict().items():
        setattr(store, store_key, store_value)
    db.commit()
    db.refresh(store)
    return store


@stores_router.delete('/store/{store_id}/')
async def store_delete(store_id: int, db: Session = Depends(get_db)):
    store = db.query(Store).filter(Store.id == store_id).first()
    if store is None:
        raise HTTPException(status_code=404, detail='store not found')
    db.delete(store)
    db.commit()
    return {'message': 'this store is deleted'}