from pydantic import BaseModel
import datetime


class NewOrderFields(BaseModel):
    products: list["OrderProduct"]


class Order(BaseModel):
    id: int
    quantity: list['Quantity']
    total_price: int
    user_id: int


class Quantity(BaseModel):
    product_id:int
    quantity:int

class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    phone_number: int
    is_active: bool
    join_date: datetime.datetime


class UserLoginCredential(BaseModel):
    username: str
    password: str


class OrderProduct(BaseModel):
    id: int
    quantity: int


class Product(BaseModel):
    id: int
    name: str
    stock: int
    price: int
    details: str
    # orders: list["Order"] | None
    categories: list['Category']

class Category(BaseModel):
    slug:str
    name:str




class NewCommentFields(BaseModel):
    text:str
    product_id:int




class ProductComment(BaseModel):
    text:str
    date:str
    is_verified:bool
    by_user:int


class ProductComments(BaseModel):
    comments:list['ProductComment']
    count:int
    total:int


class AllCategories(BaseModel):
    categories:list['Category']
    count:int
    total:int