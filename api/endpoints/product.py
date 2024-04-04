from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from dependencies import verify_user
from database.models import Product
from database.connection import engine
from api.models import (
    Product as PydanticProduct,
    Category as PydanticCategory,
    ProductComments,
    ProductComment,
    NewProductFields,
    Image as PydanticImage,
    User as PydanticUser,
)
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from dependencies import verify_user, is_super_user
from typing import Annotated
from database.models import User, Product, Order, Image, Category
from config import settings
from sqlalchemy.exc import IntegrityError
from utils.validations import is_image
from aiofiles import open as ioopen
from utils.functions import generate_sha256_hash

UserDepend = Annotated[User, Depends(verify_user)]


router = APIRouter(
    prefix="/product", tags=["product"], dependencies=[Depends(verify_user)]
)


@router.post("/new/")
async def new_product(
    product_data: NewProductFields, _: Annotated[PydanticUser, Depends(is_super_user)]
):
    with Session(engine) as ses:
        try:
            ses.begin()
            product = Product()
            product.name = product_data.name
            product.price = product_data.price
            product.stock = product_data.stock
            product.details = product_data.details
            if product_data.image_ids:
                imgs = ses.scalars(
                    select(Image).where(Image.id.in_(product_data.image_ids))
                ).all()
                product.images = imgs
            if product_data.categories:
                if isinstance(product_data.categories[0], str):
                    categories = ses.scalars(
                        select(Category).where(
                            Category.slug.in_(product_data.categories)
                        )
                    ).all()
                else:
                    categories = ses.scalars(
                        select(Category).where(Category.id.in_(product_data.categories))
                    ).all()
                product.categories = categories

            ses.add(product)

            ses.commit()

        except Exception as ex:
            ses.rollback()
            if isinstance(ex, IntegrityError):
                raise HTTPException(
                    400,
                    {
                        "code": "NAME_EXISTS",
                        "error": f"name '{product_data.name}' already exists",
                    },
                )
            print(ex)
            return JSONResponse({"code": "UNKNOWN", "error": "Unknown error"}, 500)

        cats = [
            PydanticCategory(slug=cati.slug, name=cati.name)
            for cati in product.categories
        ]
        imgs = [
            PydanticImage(id=img.id, src=img.src, hash=img.hash)
            for img in product.images
        ]
        return JSONResponse(
            PydanticProduct(
                id=product.id,
                name=product.name,
                stock=product.stock,
                price=product.price,
                details=product.details,
                categories=cats,
                images=imgs,
            ).model_dump(),
            201,
        )


@router.get("/{product_id}")
async def get_product(product_id: int):
    with Session(engine) as ses:
        product = ses.scalar(select(Product).where(Product.id == product_id))
        if not product:  # Order is not for this user or order not exists
            return JSONResponse(
                {"code": "NOT_FOUND", "error": "product not found"}, 404
            )

        categories = []
        for cat in product.categories:
            categories.append(PydanticCategory(slug=cat.slug, name=cat.name))
        return PydanticProduct(
            id=product.id,
            name=product.name,
            stock=product.stock,
            price=product.price,
            details=product.details,
            orders=None,
            categories=categories,
        )


@router.get("/{product_id}/comments/")
async def get_product_comments(product_id: int, limit: int = 10, offset: int = 0):
    if limit < 0:
        return JSONResponse(
            {"code": "BAD_LIMIT", "error": "limit can not be negative"}, 400
        )

    with Session(engine) as ses:
        total = ses.query(Product.id).count()
        product = ses.scalar(
            select(Product).where(Product.id == product_id).limit(limit).offset(offset)
        )
        if not product:  # Order is not for this user or order not exists
            return JSONResponse(
                {"code": "NOT_FOUND", "error": "product nor found"}, 404
            )

        comments = [
            ProductComment(
                text=comment.text,
                date=comment.date.strftime(settings.str_time_format),
                is_verified=comment.is_verified,
                by_user=comment.user_id,
            )
            for comment in product.comments[offset : offset + limit]
        ]

        return ProductComments(comments=comments, count=len(comments), total=total)
