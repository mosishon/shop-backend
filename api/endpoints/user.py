from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from dependencies import verify_user,verify_user_bypass_login_page
from database.models import User
from database.connection import engine
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import verify_password_hash,create_jwt_token
router = APIRouter(prefix="/user",tags=['user'],dependencies=[Depends(verify_user_bypass_login_page)])





UserDepend = Annotated[verify_user,Depends()]
@router.get("/me",response_class=JSONResponse)
async def get_me(user:UserDepend):
    return user
    
@router.post("/login",response_class=JSONResponse)
async def user_login(login_credential:Annotated[OAuth2PasswordRequestForm,Depends()]):
    with Session(engine) as ses,ses.begin():
        user = ses.scalar(select(User).where(User.username == login_credential.username))
        if user and verify_password_hash(login_credential.password,user.password):
            token = create_jwt_token({"uid":user.id})
            return {"access_token":token,"token_type":"bearer"}
        raise HTTPException(401,"Unauthorized")

