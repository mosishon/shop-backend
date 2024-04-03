from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from dependencies import verify_user
from database.models import User
from database.connection import engine
from typing import Annotated
from api.models import UserLoginCredential
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import verify_password_hash,create_jwt_token
router = APIRouter(prefix="/user",tags=['user'],dependencies=[Depends(verify_user)])





UserDepend = Annotated[User,Depends(verify_user)]
@router.get("/me",response_class=JSONResponse)
async def get_me(user:UserDepend):
    return user
    
@router.post("/login",response_class=JSONResponse)
async def user_login(login_credential:UserLoginCredential):
    with Session(engine) as ses,ses.begin():
        user = ses.scalar(select(User).where(User.username == login_credential.username))
        if user and verify_password_hash(login_credential.password,user.password):
            token = create_jwt_token({"uid":user.id})
            return {"token":token}
        

