from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from glovo_app.db.models import StoreReview
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import StoreReviewSchema


store_review_router = APIRouter(prefix='/auth', tags=['Auth'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# store_review
@store_review_router.post('/store_review/create/', response_model=StoreReviewSchema)
async def store_review_create(store_review: StoreReviewSchema, db: Session = Depends(get_db)):
    store_review_db = StoreReview(**store_review.dict())
    db.add(store_review_db)
    db.commit()
    db.refresh(store_review_db)
    return store_review_db


@store_review_router.get('/store_review/', response_model=List[StoreReviewSchema])
async def store_review_list(db: Session = Depends(get_db)):
    return db.query(StoreReview).all()


@store_review_router.get('/store_review/{store_review_id}/', response_model=StoreReviewSchema)
async def store_review_detail(store_review_id: int, db: Session = Depends(get_db)):
    store_review = db.query(StoreReview).filter(StoreReview.id == store_review_id).first()
    if store_review is None:
        raise HTTPException(status_code=404, detail='store_review not found')
    return store_review


@store_review_router.put('/store_review/{store_review_id}/', response_model=StoreReviewSchema)
async def store_review_update(store_review_id: int, store_review_data: StoreReviewSchema, db: Session = Depends(get_db)):
    store_review = db.query(StoreReview).filter(StoreReview.id == store_review_id).first()
    if store_review is None:
        raise HTTPException(status_code=404, detail='store_review not found')
    for store_review_key, store_review_value in store_review_data.dict().items():
        setattr(store_review, store_review_key, store_review_value)
    db.commit()
    db.refresh(store_review)
    return store_review


@store_review_router.delete('/store_review/{store_review_id}/')
async def store_review_delete(store_review_id: int, db: Session = Depends(get_db)):
    store_review = db.query(StoreReview).filter(StoreReview.id == store_review_id).first()
    if store_review is None:
        raise HTTPException(status_code=404, detail='store_review not found')
    db.delete(store_review)
    db.commit()
    return {'message': 'this store_review is deleted'}