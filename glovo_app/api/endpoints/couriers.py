from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from glovo_app.db.models import Courier
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import CourierSchema


courier_router = APIRouter(prefix='/auth', tags=['Auth'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# courier
@courier_router.post('/courier/create/', response_model=CourierSchema)
async def courier_create(courier: CourierSchema, db: Session = Depends(get_db)):
    courier_db = Courier(**courier.dict())
    db.add(courier_db)
    db.commit()
    db.refresh(courier_db)
    return courier_db


@courier_router.get('/courier/', response_model=List[CourierSchema])
async def courier_list(db: Session = Depends(get_db)):
    return db.query(Courier).all()


@courier_router.get('/courier/{courier_id}/', response_model=CourierSchema)
async def courier_detail(courier_id: int, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier is None:
        raise HTTPException(status_code=404, detail='courier not found')
    return courier


@courier_router.put('/courier/{courier_id}/', response_model=CourierSchema)
async def courier_update(courier_id: int, courier_data: CourierSchema, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier is None:
        raise HTTPException(status_code=404, detail='courier not found')
    for courier_key, courier_value in courier_data.dict().items():
        setattr(courier, courier_key, courier_value)
    db.commit()
    db.refresh(courier)
    return courier


@courier_router.delete('/courier/{courier_id}/')
async def courier_delete(courier_id: int, db: Session = Depends(get_db)):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier is None:
        raise HTTPException(status_code=404, detail='courier not found')
    db.delete(courier)
    db.commit()
    return {'message': 'this courier is deleted'}