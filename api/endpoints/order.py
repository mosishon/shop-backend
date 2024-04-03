from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from dependencies import verify_user
from database.models import Product,Order
from database.connection import engine
from api.models import NewOrderFields,Order as PydanticOrder,Quantity as PydanticQuantity
from sqlalchemy import select
from sqlalchemy.orm import Session
import ujson as json
from dependencies import verify_user
from typing import Annotated
from database.models import User,Product,Order


UserDepend = Annotated[User,Depends(verify_user)]


router = APIRouter(prefix="/order",tags=['order'],dependencies=[Depends(verify_user)])


@router.post("/new",tags=['order'])
async def new_order(order:NewOrderFields,user:UserDepend):
    with Session(engine) as ses:
        if len(order.products) == 0:

            return {"error":"products list is empty","code":"PRODUCTS_IS_EMPTY"}
        products = []
        counts = {}
        total_price = 0
        try:
            ses.begin()
            for product in order.products:
                product_instance = ses.scalar(select(Product).where(Product.id == product.id))
                if not product_instance:
                    return {"error":f"product with id {product.id} not found","code":"PRODUCTS_IS_EMPTY"}
                products.append(product_instance)
                counts[product.id] = product.quantity
                total_price += (product_instance.price * product.quantity)
            new_order_instance = Order()
            new_order_instance.products = products
            new_order_instance.quantity = json.dumps(counts)
            new_order_instance.total_price = total_price
            new_order_instance.user_id = user.id
            ses.add(new_order_instance)
        except:
            ses.rollback()
            return JSONResponse({"code":"UNKNOWN","error":"Unknown error"},500)

        else:
            ses.commit()
            
        return JSONResponse({"code":"CREATED","order_id":new_order_instance.id},201)

                


@router.get("/{order_id}",tags=['order'])
async def get_order(order_id:int,user:UserDepend):
    with Session(engine) as ses:
        order = ses.scalar(select(Order).where(Order.id == order_id))
        if not order or order.user_id != user.id: #Order is not for this user or order not exists
            return {"code":"NOT_FOUND","error":"order nor found"}
        quantity = json.loads(order.quantity)
        quantites = []
        
        for key in quantity:
            q = PydanticQuantity(product_id=int(quantity[key]),quantity=int(key))
            quantites.append(q)
        return PydanticOrder(id=order.id,quantity=quantites,total_price=order.total_price,user_id=user.id)