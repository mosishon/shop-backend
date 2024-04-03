from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from dependencies import verify_user
from database.models import Product
from database.connection import engine
from api.models import Product as PydanticProduct,Order as PydanticOrder,Quantity,Category as PydanticCategory,ProductComments,ProductComment
from sqlalchemy import select,func
from sqlalchemy.orm import Session
import ujson as json
from dependencies import verify_user
from typing import Annotated
from database.models import User,Product,Order
from config import settings

UserDepend = Annotated[User,Depends(verify_user)]


router = APIRouter(prefix="/product",tags=['product'],dependencies=[Depends(verify_user)])

#TODO new product should be by super user




@router.get("/{product_id}")
async def get_product(product_id:int):
    with Session(engine) as ses:
        product = ses.scalar(select(Product).where(Product.id == product_id))
        if not product: #Order is not for this user or order not exists
            return JSONResponse({"code":"NOT_FOUND","error":"product not found"},404)

        categories = []
        for cat in product.categories:
            categories.append(PydanticCategory(slug=cat.slug,name=cat.name))
        return PydanticProduct(id=product.id,name=product.name,stock=product.stock,price=product.price,details=product.details,orders=None,categories=categories)
    


@router.get("/{product_id}/comments/")
async def get_product_comments(product_id:int,limit:int=10,offset:int=0):
    if limit<0:
        return JSONResponse({"code":"BAD_LIMIT","error":"limit can not be negative"},400)

    with Session(engine) as ses:
        total = ses.query(Product.id).count()
        product = ses.scalar(select(Product).where(Product.id == product_id).limit(limit).offset(offset))
        if not product: #Order is not for this user or order not exists
            return JSONResponse({"code":"NOT_FOUND","error":"product nor found"},404)

        comments = [ProductComment(text=comment.text,date=comment.date.strftime(settings.str_time_format),is_verified=comment.is_verified,by_user=comment.user_id) for comment in product.comments[offset:offset+limit]]

        return ProductComments(comments=comments,count=len(comments),total=total)