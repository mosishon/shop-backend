from fastapi import Depends, HTTPException, Request
from api.models import User as PydanticUserModel
from auth import verify_jwt_token, oauth_user_schema
import time
from config import settings

from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import User
from database.connection import engine


async def verify_user(
    request:Request,
) -> PydanticUserModel | None:
    if request.url != request.url_for("user_login"):
        jwt_token:str = await oauth_user_schema(request)
        dict_data = verify_jwt_token(jwt_token)
        if not dict_data:
            raise HTTPException(401, "Unauthorized")
        expire = dict_data["exp"]
        now = time.time()
        if now - expire > settings.jwt_expire_after_minute * 60:
            raise HTTPException(401, "Unauthorized")
        user_id = dict_data.get("uid", -1)
        with Session(engine) as session:
            user = session.scalar(select(User).where(User.id == user_id))
            if user:
                return PydanticUserModel(
                    id=user.id,
                    name=user.name,
                    username=user.username,
                    email=user.email,
                    phone_number=user.phone_number,
                    join_date=user.join_date,
                    is_active=user.is_active,
                )
            else:
                raise HTTPException(401, "Unauthorized")

