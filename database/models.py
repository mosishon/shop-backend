from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import Table, Column

from sqlalchemy import ForeignKey
import datetime
from database.connection import engine


class Base(DeclarativeBase):
    pass


# for many to many relations
OrdersAssoiation = Table(
    "orders_association",
    Base.metadata,
    Column("product_id", ForeignKey("products.id")),
    Column("order_id", ForeignKey("orders.id")),
)

ProductsAssoiation = Table(
    "products_association",
    Base.metadata,
    Column("product_id", ForeignKey("products.id")),
    Column("category_id", ForeignKey("categories.id")),
)
ImagesAssoiation = Table(
    "images_association",
    Base.metadata,
    Column("product_id", ForeignKey("products.id")),
    Column("image_id", ForeignKey("images.id")),
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    phone_number: Mapped[int] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    join_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    is_super_user: Mapped[bool] = mapped_column(default=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="user")


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)
    products: Mapped[list["Product"]] = relationship(
        secondary=ProductsAssoiation, back_populates="categories"
    )


class Image(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(primary_key=True)
    src: Mapped[str] = mapped_column(unique=True)
    hash: Mapped[str] = mapped_column(unique=True)

    upload_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )
    upload_by_user: Mapped["User"] = relationship()
    upload_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    products: Mapped[list["Product"]] = relationship(
        secondary=ImagesAssoiation, back_populates="images"
    )


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    stock: Mapped[int] = mapped_column(default=0)
    price: Mapped[int] = mapped_column()
    details: Mapped[str] = mapped_column()
    orders: Mapped[list["Order"]] = relationship(
        secondary=OrdersAssoiation, back_populates="products"
    )
    categories: Mapped[list["Category"]] = relationship(
        secondary=ProductsAssoiation, back_populates="products"
    )
    comments: Mapped[list["Comment"]] = relationship(back_populates="product")
    images: Mapped[list["Image"]] = relationship(
        secondary=ImagesAssoiation, back_populates="products",cascade="all,delete-orphan"
    )
    update_date: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now
    )


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    is_verified: Mapped[bool] = mapped_column(
        default=False
    )  # verified by admin to show
    product: Mapped[Product] = relationship(back_populates="comments")
    user: Mapped[User] = relationship()
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[str] = mapped_column()  # str(json) for quantity
    total_price: Mapped[int] = mapped_column()

    user: Mapped[User] = relationship(back_populates="orders")
    products: Mapped[list["Product"]] = relationship(
        secondary=OrdersAssoiation, back_populates="orders"
    )

    user_id: Mapped[int] = mapped_column(ForeignKey(f"{User.__tablename__}.id"))


from sqlalchemy.orm import Session


def create_new_user(
    name: str,
    email: str,
    phone_number: int,
    username: str,
    password: str,
    is_active: bool = None,
    join_date: datetime.datetime = None,
):
    from auth import create_password_hash
    
    password = create_password_hash(password)
    user = User(
        name=name,
        email=email,
        phone_number=phone_number,
        username=username,
        password=password,
        is_active=is_active,
        join_date=join_date,
    )
    with Session(engine) as ses, ses.begin():
        ses.add(user)
    return user


def new_product(
    session: Session,
    name: str,
    stock: int,
    price: int,
    details: str,
    categories: list[Category],
    orders: list[Order] = None,
):
    prod = Product(name=name, stock=stock, price=price, details=details, orders=orders)
    prod.categories.extend(categories)
    print(prod)
    print(prod.categories)
    session.add(prod)
    return prod


def new_category(session: Session, slug, name, products):
    cat = Category(slug=slug, name=name, products=products)
    session.add(cat)
    return cat


Base.metadata.create_all(engine)

# create_new_user("mostafa arshadi","mostafa.arshadi@outlook.com",9164230882,"mosishon","fuckingpass",True,datetime.datetime.now())
# with Session(engine) as ses,ses.begin():
#     cat1 = Category(slug="slug_1",name="slug1")
#     cat2 = Category(slug="slug_2",name="slug2")
#     cat3 = Category(slug="slug_3",name="slug3")
#     prod = Product(name="name",stock=2,price=450000,details="heloo details",orders=[],categories=[cat1,cat2,cat3])


#     ses.add_all([cat1,cat2,cat3,prod])
