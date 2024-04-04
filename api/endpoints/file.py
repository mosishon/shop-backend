from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from dependencies import verify_user
from database.models import Product
from database.connection import engine
from api.models import (
    Product as PydanticProduct,
    Order as PydanticOrder,
    Quantity,
    Category as PydanticCategory,
    ProductComments,
    ProductComment,
    NewProductFields,
    Image as PydanticImage,
    User as PydanticUser,
    UploadImageFields,
)
from sqlalchemy import select, func
from sqlalchemy.orm import Session
import ujson as json
from dependencies import verify_user, is_super_user
from typing import Annotated
from database.models import User, Product, Order, Image, Category
from config import settings
from sqlalchemy.exc import IntegrityError
from utils.validations import is_image
import asyncio
import uuid
import os
from aiofiles import open as ioopen
from utils.functions import generate_sha256_hash

UserDepend = Annotated[User, Depends(verify_user)]

router = APIRouter(prefix="/file", tags=["file"], dependencies=[Depends(verify_user)])


@router.post("/upload_image/")
async def upload_image(
    file: UploadFile, user: Annotated[PydanticUser, Depends(is_super_user)]
):
    is_image_ = await asyncio.get_running_loop().run_in_executor(
        None, is_image, file.file
    )
    if not is_image_:
        return HTTPException(
            400,
            {"code": "FILE_FORMAT_WRONG", "error": "file is not a valid image file"},
        )
    img_hash = await asyncio.get_running_loop().run_in_executor(
        None, generate_sha256_hash, file.file
    )
    with Session(engine) as ses:
        img = ses.scalar(select(Image).where(Image.hash == img_hash))
        if img:
            return PydanticImage(id=img.id, src=img.src, hash=img_hash)
    file.file.seek(0)
    fformat = "." + file.filename.split(".")[-1].strip()
    fname = str(uuid.uuid4()).replace("-", "") + fformat
    fpath = os.path.relpath(os.path.join(settings.static_files_path, fname))

    async with ioopen(fpath, "wb") as f:
        while data := file.file.read(1024 * 50):
            await f.write(data)
    with Session(engine) as ses:
        ses.begin()
        try:
            new_image_instance = Image()
            new_image_instance.src = fpath
            new_image_instance.upload_by_user_id = user.id
            new_image_instance.hash = img_hash
            ses.add(new_image_instance)
            ses.commit()
            return PydanticImage(
                id=new_image_instance.id,
                src=new_image_instance.src,
                hash=new_image_instance.hash,
            )
        except:
            ses.rollback()
