from fastapi import APIRouter

from api.carts.routes import router as carts_router
from api.checkouts.routes import router as checkouts_router
from api.customers.routes import router as customers_router
from api.offers.routes import router as offers_router
from api.products.routes import router as products_router

api_v1_router = APIRouter()
api_v1_router.include_router(customers_router, prefix="/customers", tags=["Customers"])
api_v1_router.include_router(products_router, prefix="/products", tags=["Products"])
api_v1_router.include_router(offers_router, prefix="/offers", tags=["Offers"])
api_v1_router.include_router(carts_router, prefix="/carts", tags=["Carts"])
api_v1_router.include_router(checkouts_router, prefix="/checkouts", tags=["Checkouts"])
