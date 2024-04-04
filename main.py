from fastapi import FastAPI
from config import settings
import os
from api.endpoints.user import router as user_router
from api.endpoints.order import router as order_router
from api.endpoints.product import router as product_router
from api.endpoints.comment import router as comment_router
from api.endpoints.category import router as category_router
from api.endpoints.file import router as file_router



if not os.path.exists(settings.static_files_path):
    os.makedirs(settings.static_files_path)

os.environ['TZ'] = settings.timezone

if settings.env=="debug":
    print("RUNNING DEBUG")

application = FastAPI(debug=settings.env=="debug")

application.include_router(user_router,prefix='/api/v1')
application.include_router(order_router,prefix='/api/v1')
application.include_router(product_router,prefix='/api/v1')
application.include_router(comment_router,prefix='/api/v1')
application.include_router(category_router,prefix='/api/v1')
application.include_router(file_router,prefix='/api/v1')
    