from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependencies import verify_user
from database.models import Category
from database.connection import engine
from api.models import Category as PydanticCategory, AllCategories,NewCategoryFields
from sqlalchemy import select
from sqlalchemy.orm import Session
from dependencies import verify_user
from typing import Annotated
from database.models import User
from utils.validations import is_slug



UserDepend = Annotated[User, Depends(verify_user)]


router = APIRouter(
    prefix="/category", tags=["category"], dependencies=[Depends(verify_user)]
)

@router.post("/new/")
async def new_category(category:NewCategoryFields):
    if not is_slug(category.slug):
        return JSONResponse(
            {"code":"INVALID_SLUG","error":"slug is not valid"}
        )
    with Session(engine) as ses:
        ses.begin()
        try:
            new_category_instance = Category()
            new_category_instance.name = category.name
            new_category_instance.slug = category.slug
            ses.add(new_category_instance)
            ses.commit()
            return PydanticCategory(slug=new_category_instance.slug, name=new_category_instance.name)
        except Exception as ex:
            ses.rollback()
            return JSONResponse(
                {"code":"UNKNOWN","error":"unknown error"},500
            )
        
            

@router.get("/{category_id}")
async def get_category_by_id(category_id: int):
    with Session(engine) as ses:
        category = ses.scalar(select(Category).where(Category.id == category_id))
        if not category:  # Order is not for this user or order not exists
            return JSONResponse(
                {"code": "NOT_FOUND", "error": "category not found"}, 404
            )

        return PydanticCategory(slug=category.slug, name=category.name)


@router.get("/{category_slug}")
async def get_category_by_slug(category_slug: str):
    with Session(engine) as ses:
        category = ses.scalar(select(Category).where(Category.slug == category_slug))
        if not category:  # Order is not for this user or order not exists
            return JSONResponse(
                {"code": "NOT_FOUND", "error": "category not found"}, 404
            )

        return PydanticCategory(slug=category.slug, name=category.name)


@router.get("/all/")
async def get_all_categories(limit: int = 10, offset: int = 0):
    if limit < 0:
        return JSONResponse(
            {"code": "BAD_LIMIT", "error": "limit can not be negative"}, 400
        )
    with Session(engine) as ses:
        total = ses.query(Category.id).count()
        cats = ses.scalars(select(Category).limit(limit).offset(offset))
        categories = [
            PydanticCategory(slug=category.slug, name=category.name)
            for category in cats
        ]
        return AllCategories(categories=categories, count=len(categories), total=total)
