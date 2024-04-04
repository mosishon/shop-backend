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
from api.models import UserUpdateInfo,User as PydanticUser
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

@router.patch("/update_info/")
async def update_info(update_data:UserUpdateInfo,user:UserDepend):
    with Session(engine) as ses:
        ses.begin()
        check_exists = ses.query(User.id).where(User.username == update_data.username).count()
        if check_exists>0:
            return JSONResponse(
                {"code":"USERNAME_TAKEN","error":f"username {update_data.username} already taken."},400
            )
        try:
            user_instance = ses.scalar(select(User).where(User.id == user.id))
            for field in update_data.model_fields.keys():
                if hasattr(user_instance,field) and getattr(update_data,field)!=None:
                    setattr(user_instance,field,getattr(update_data,field))
            ses.commit()
        except Exception as ex:
            ses.rollback()
            return JSONResponse(
                {"code": "UNKNOWN", "error": "Unknown error"}, 500
            )

    return JSONResponse(
        {"code":"USER_UPDATED","update_fields":[i for i in update_data.model_fields if getattr(update_data,i) != None]}
    )