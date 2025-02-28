from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from glovo_app.db.models import CourierReview
from glovo_app.db.database import SessionLocal
from glovo_app.db.schema import CourierReviewSchema


courier_review_router = APIRouter(prefix='/auth', tags=['Auth'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# courier_review
@courier_review_router.post('/courier_review/create/', response_model=CourierReviewSchema)
async def courier_review_create(courier_review: CourierReviewSchema, db: Session = Depends(get_db)):
    courier_review_db = CourierReview(**courier_review.dict())
    db.add(courier_review_db)
    db.commit()
    db.refresh(courier_review_db)
    return courier_review_db


@courier_review_router.get('/courier_review/', response_model=List[CourierReviewSchema])
async def courier_review_list(db: Session = Depends(get_db)):
    return db.query(CourierReview).all()


@courier_review_router.get('/courier_review/{courier_review_id}/', response_model=CourierReviewSchema)
async def courier_review_detail(courier_review_id: int, db: Session = Depends(get_db)):
    courier_review = db.query(CourierReview).filter(CourierReview.id == courier_review_id).first()
    if courier_review is None:
        raise HTTPException(status_code=404, detail='courier_review not found')
    return courier_review


@courier_review_router.put('/courier_review/{courier_review_id}/', response_model=CourierReviewSchema)
async def courier_review_update(courier_review_id: int, courier_review_data: CourierReviewSchema,
                                db: Session = Depends(get_db)):
    courier_review = db.query(CourierReview).filter(CourierReview.id == courier_review_id).first()
    if courier_review is None:
        raise HTTPException(status_code=404, detail='courier_review not found')
    for courier_review_key, courier_review_value in courier_review_data.dict().items():
        setattr(courier_review, courier_review_key, courier_review_value)
    db.commit()
    db.refresh(courier_review)
    return courier_review


@courier_review_router.delete('/courier_review/{courier_review_id}/')
async def courier_review_delete(courier_review_id: int, db: Session = Depends(get_db)):
    courier_review = db.query(CourierReview).filter(CourierReview.id == courier_review_id).first()
    if courier_review is None:
        raise HTTPException(status_code=404, detail='courier_review not found')
    db.delete(courier_review)
    db.commit()
    return {'message': 'this courier_review is deleted'}