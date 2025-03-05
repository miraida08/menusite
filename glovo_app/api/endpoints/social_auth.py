from sqlalchemy.orm import Session
from glovo_app.db.database import SessionLocal
from fastapi import APIRouter
from starlette.requests import Request
from glovo_app.config import settings
from authlib.integrations.starlette_client import OAuth


social_router = APIRouter(prefix='/oauth', tags=['Social_auth'])

oauth = OAuth()
oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    secret_key=settings.GITHUB_KEY,
    authorize_url="https://github.com/login/oauth/authorize"
)
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    secret_key=settings.GOOGLE_KEY,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    client_kwargs={'scope': 'openid profile email'}


)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@social_router.get('/github/')
async def github_login(request: Request):
    redirect_uri = settings.GITHUB_URL
    return await oauth.github.authorize_redirect(request, redirect_uri)


@social_router.get('/google/')
async def google_login(request: Request):
    redirect_uri = settings.GOOGLE_URL
    return await oauth.google.authorize_redirect(request, redirect_uri)



