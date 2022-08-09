import table_define
import user_ops
from fastapi import FastAPI
from signup import engine
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication

# from
# from store_db import item

app = FastAPI()
app.include_router(user_ops.router)
app.include_router(authentication.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/data")
def read_root():
    return {"Hello": "World"}


# @app.post("/newuser")
# def signup(db:UserBase):


table_define.Base.metadata.create_all(engine)
