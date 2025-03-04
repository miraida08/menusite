import fastapi
import redis.asyncio as redis
import uvicorn
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from contextlib import asynccontextmanager
from fastapi import FastAPI
from admin.setup import setup_admin
from api.endpoints import (auth, categories, courier_reviews, couriers, orders, products, product_comdos,
                           store_reviews, stores, social_auth)
from starlette.middleware.sessions import SessionMiddleware
from glovo_app.config import SECRET_KEY

async def init_redis():
    return redis.Redis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


glovo_app = fastapi.FastAPI(title='glovo_site', lifespan=lifespan)
glovo_app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")
setup_admin(glovo_app)

glovo_app.include_router(auth.auth_router, tags=['Auth'])
glovo_app.include_router(categories.category_router, tags=['Categories'])
glovo_app.include_router(couriers.courier_router, tags=['Couriers'])
glovo_app.include_router(courier_reviews.courier_review_router, tags=['Courier_reviews'])
glovo_app.include_router(orders.order_router, tags=['Orders'])
glovo_app.include_router(product_comdos.product_combo_router, tags=['Product_combos'])
glovo_app.include_router(products.product_router, tags=['Products'])
glovo_app.include_router(stores.stores_router, tags=['Stores'])
glovo_app.include_router(store_reviews.store_review_router, tags=['Store_reviews'])
glovo_app.include_router(social_auth.social_router, tags=['social'])

if __name__ == '__main__':
    uvicorn.run(glovo_app, host='127.0.0.1', port=8080)






