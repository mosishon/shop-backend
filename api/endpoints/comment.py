from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependencies import verify_user
from database.models import Product, Comment
from database.connection import engine
from api.models import (
    NewCommentFields,
)
from sqlalchemy import select
from sqlalchemy.orm import Session
from dependencies import verify_user
from typing import Annotated
from database.models import User, Product
import datetime
import pytz
from config import settings

UserDepend = Annotated[User, Depends(verify_user)]


router = APIRouter(
    prefix="/comment", tags=["comment"], dependencies=[Depends(verify_user)]
)


@router.post("/new/")
async def new_comment(comment: NewCommentFields, user: UserDepend):
    with Session(engine) as ses:
        ses.begin()
        prod = ses.scalar(select(Product).where(Product.id == comment.product_id))
        if not prod:
            return JSONResponse(
                {
                    "error": f"product with id {comment.product_id} not exists",
                    "code": "PRODUCT_NOT_FOUND",
                },
                404,
            )
        new_comment_instance = Comment()
        new_comment_instance.date = datetime.datetime.now(
            pytz.timezone(settings.timezone)
        )
        new_comment_instance.product = prod
        new_comment_instance.user_id = user.id
        new_comment_instance.text = comment.text
        try:
            ses.add(new_comment_instance)
        except Exception as ex:
            ses.rollback()
            return JSONResponse(
                {"code": "UNKNOWN", "error": "Unknown error:" + str(ex)}, 500
            )

        else:
            ses.commit()
            return JSONResponse(
                {"code": "CREATED", "comment_id": new_comment_instance.id}, 201
            )


@router.get("/{comment_id}")
async def get_comment(comment_id: int):
    with Session(engine) as ses:
        comment = ses.scalar(select(Comment).where(Comment.id == comment_id))
        if not comment:  # Order is not for this user or order not exists
            return JSONResponse(
                {"code": "NOT_FOUND", "error": "comment not found"}, 404
            )

        return JSONResponse(
            NewCommentFields(
                text=comment.text, product_id=comment.product_id
            ).model_dump(),
            200,
        )
