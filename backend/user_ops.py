# from tabel_define import DbUser
from ast import For
from regex import F
import table_define
from crud import create_user, get_all_items,create_item,update_item,add_quantity
from crud import get_price,get_all_items,sell_item,delete_an_item,add_customers,is_quantity_available
from fastapi import APIRouter, Depends
from schemas import GetUser,GetPrice,ItemBase, UserBase,DeleteItem,CustomerDetails,ForQuantity
from signup import engine, get_db
from sqlalchemy.orm import Session 
from auth.oauth2 import get_current_user
from fastapi.responses import RedirectResponse
from fastapi import status
from typing import List

router = APIRouter(prefix="", tags=["user"])

@router.post("/signup")
def insert_user(request: UserBase, db: Session = Depends(get_db)):
    return create_user(db, request)

# @router.post("/login") 
# def get_users(request: GetUser = Depends(get_current_user), db: Session = Depends()):
#     get_user_table(request) 
#     return "ok"

@router.post("/all_items") 
def get_all(db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return get_all_items(db)

@router.post("/add_item")
def add_item(request: ItemBase, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return create_item(db,request)

@router.post("/update_items")
def updat_item(request: ItemBase, db: Session = Depends(get_db),current_user = Depends(get_current_user)):
    return update_item(db,request)
    
@router.post("/sell")
def sell_an_item(request:ItemBase,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return sell_item(db,request)

@router.post("/delete")
def delete_items(request:DeleteItem,db:Session = Depends(get_db),current_user = Depends(get_current_user)):
    return delete_an_item(db,request)

# @router.get("/logout")
# def logout(token:str):
#   response = RedirectResponse('*your login page*', status_code= 302)
#   response.delete_cookie(key = token)
#   return response

@router.post("/getprice")
def get_pre(request:GetPrice,db:Session = Depends(get_db)):
    print("oksad")
    return get_price(request,db)

@router.post("/getcustomerdetails")
def savecustomer(request:CustomerDetails,db:Session = Depends(get_db)):
    return add_customers(request,db)

@router.post("/removequantity")
def getquantity(request:ForQuantity,db:Session = Depends(get_db)):
    return is_quantity_available(request,db) 

@router.post("/addquantity")
def updatequantity(request:ForQuantity,db:Session = Depends(get_db)):
    return add_quantity(db,request)

# @router.get('/logout')
# def logout():
#     if "username" in Session:
#         Session.pop('username',None)
#     else:
#         return "not ok"
#     return "ok"


# table_define.Base.metadata.create_all(engine)
