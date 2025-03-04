from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from glovo_app.db.models import Order
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import OrderSchema


order_router = APIRouter(prefix='/order', tags=['Orders'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# order
@order_router.post('/order/create/', response_model=OrderSchema)
async def order_create(order: OrderSchema, db: Session = Depends(get_db)):
    order_db = Order(**order.dict())
    db.add(order_db)
    db.commit()
    db.refresh(order_db)
    return order_db


@order_router.get('/order/', response_model=List[OrderSchema])
async def order_list(db: Session = Depends(get_db)):
    return db.query(Order).all()


@order_router.get('/order/{order_id}/', response_model=OrderSchema)
async def order_detail(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='order not found')
    return order


@order_router.put('/order/{order_id}/', response_model=OrderSchema)
async def order_update(order_id: int, order_data: OrderSchema, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='order not found')
    for order_key, order_value in order_data.dict().items():
        setattr(order, order_key, order_value)
    db.commit()
    db.refresh(order)
    return order


@order_router.delete('/order/{order_id}/')
async def order_delete(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='order not found')
    db.delete(order)
    db.commit()
    return {'message': 'this order is deleted'}