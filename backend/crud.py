from fastapi import HTTPException

from schemas import GetUser, ItemBase,GetPrice,UserBase,DeleteItem,CustomerDetails,ForQuantity
from signup import engine
from sqlalchemy import MetaData, Table, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import Session
from table_define import Base, DbUser, create_customers_table,create_table
from typing import List
import table_define
from hashing import Hash

def create_user(db: Session, request: UserBase):
    anyuser = db.query(DbUser).filter(DbUser.userid == request.userid )
    if anyuser.first() is None:
        new_user = DbUser(
            name=request.name,
            password=Hash.bcrypt(request.password),
            contact=request.contact,
            userid=request.userid,
        ) 
        create_table(request)
        create_customers_table(request)
        table_define.Base.metadata.create_all(engine)
        db.add(new_user)        
        db.commit()   
        db.refresh(new_user)
        return "ok"
    else:
        return "*There was already a user with this userId please try another"  


# def get_user_table(request:GetUser):
#     global Rand
#     items_table = Table(request.username, MetaData(), autoload_with=engine)
#     class Rand(Base):
#         __table__ = items_table

def get_user_table(username:str):
    global ItemTable
    global CustomerTable
    items_table = Table(username, MetaData(), autoload_with=engine)
    class ItemTable(Base):
        __table__ = items_table
    
    cust_table = Table(username+"customers",MetaData(),autoload_with = engine)
    class CustomerTable(Base):
        __table__ = cust_table



def get_user(db: Session, request: ItemBase):
    user = (
        db.query(DbUser)
        .filter(DbUser.userid == request.userid and DbUser.password == request.password)
        .first()
    )
    if user == None:
        return "please signup"
    else:
        return "ok"

def get_price(request:GetPrice,db:Session):

    item = db.query(ItemTable).filter(ItemTable.name == request.itemname.upper()+request.metric.lower())
    if item.first():
        return {"price":item.first().price}
    else:
        return f"{request.itemname} was not available"

def is_quantity_available(request:ForQuantity,db:Session):
    item = db.query(ItemTable).filter(ItemTable.name == request.name.upper()+request.metric.lower())
    if item.first() is not None:
        if item.first().quantity >= request.quantity :
            item.update({
                ItemTable.quantity:ItemTable.quantity-request.quantity
            })
            db.commit()
            return "valid"
        else:
            return f"{request.name} only {str(item.first().quantity)+request.metric.lower()} where available" 
    else:
        return f"{request.name} was not available"
        # raise HTTPException(status_code = 404,detail= f"{request.name} was not available")

def add_customers(request:CustomerDetails,db:Session):
    customer = db.query(CustomerTable).filter(CustomerTable.contact == request.contact)
    if customer.first():
        customer.update({
            CustomerTable.shopvalue:request.shopvalue+CustomerTable.first().shopvalue
        })
        print('not ok')
        return "ok"
    else:
        new_customer = CustomerTable(
            name = request.cust_name,
            contact = request.contact,
            shopvalue = request.shopvalue
        )
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return "ok"


def create_item(db:Session,request:ItemBase):
    item = db.query(ItemTable).filter(ItemTable.name == request.name.upper()+request.metric.lower())
    if item.first() is None:
        new_item = ItemTable(
            name=request.name.upper()+request.metric.lower(),
            quantity = request.quantity,
            price = request.price
        )
        db.add(new_item)
        db.commit() 
        db.refresh(new_item)
        return f"item {request.name} added"
    else:
        return f"item {request.name} is already there"


def get_all_items(db:Session):
    return db.query(ItemTable).all()


def update_item(db:Session,request:ItemBase):
    item = db.query(ItemTable).filter(ItemTable.name == request.name.upper()+request.metric.lower())
    
    if item.first() is not None:
        item.update({
            ItemTable.quantity:request.quantity +item.first().quantity,
            ItemTable.price: request.price
        })
        db.commit()
        return f"item {request.name} was updated"
    else:
        return f"item {request.name} not yet added"

def sell_item(db:Session,request:ItemBase):
    item = db.query(ItemTable).filter(ItemTable.name == request.name.upper()+request.metric.lower())
    if item.first() is not None:
        item.update({
            ItemTable.quantity: item.first().quantity - request.quantity,
        })
        db.commit()
    else:
        return f"item {request.name} was not available"
    return "ok"

def delete_an_item(db:Session,request:DeleteItem):
    try:
        item = db.query(ItemTable).filter(ItemTable.name == request.name.upper()+request.metric.lower()).first()
        db.delete(item)
        db.commit()
        return f"item {request.name} deleted"
    except:
        return "something went wrong"



def add_quantity(db:Session,request:ForQuantity):
    item = db.query(ItemTable).filter(ItemTable.name == request.name.upper()+request.metric.lower())
    item.update({
        ItemTable.quantity : item.one().quantity+request.quantity
    })
    db.commit()
    print("fine")
    return "ok"


