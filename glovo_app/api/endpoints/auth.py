from glovo_app.db.schema import UserProfileSchema
from glovo_app.db.models import UserProfile, RefreshToken
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from glovo_app.db.database import SessionLocal

from glovo_app.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, ALGORITHM
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi_limiter.depends import RateLimiter
from passlib.hash import bcrypt

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def set_password(self, password: str):
    self.hashed_password = bcrypt.hash(password)

    # login


def check_password(self, password: str):
    return bcrypt.verify(password, self.hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refesh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_router.post('/register/')
async def register(user: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if user_db:
        raise HTTPException(status_code=400, detail='username бар экен')
    new_hash_pass = get_password_hash(user.password)
    new_user = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone_number=user.phone_number,
        role=user.role,
        hashed_password=new_hash_pass
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": 'Saved'}


@auth_router.post('/login', dependencies=[Depends(RateLimiter(times=3, seconds=200))])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Маалымат туура эмес')
    access_token = create_access_token({'sub': user.username})
    refresh_token = create_refesh_token({'sub': user.username})

    user_db = RefreshToken(token=refresh_token, user_id=user.id)
    db.add(user_db)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


@auth_router.post('/logout/')
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Маалымат туура эмес")
    db.delete(stored_token)
    db.commit()
    return {"message": "Сайттан чыктыныз"}