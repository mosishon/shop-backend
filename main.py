from fastapi import FastAPI,APIRouter,Request
from config import settings
import os
from api.endpoints.user import router as user_router
from api.endpoints.order import router as order_router
from api.endpoints.product import router as product_router
from api.endpoints.comment import router as comment_router
from api.endpoints.category import router as category_router




os.environ['TZ'] = settings.timezone



application = FastAPI(debug=settings.env=="debug")

application.include_router(user_router,prefix='/api/v1')
application.include_router(order_router,prefix='/api/v1')
application.include_router(product_router,prefix='/api/v1')
application.include_router(comment_router,prefix='/api/v1')
application.include_router(category_router,prefix='/api/v1')
    