from fastapi import FastAPI
from api.router import router

app = FastAPI()
app.include_router(router)


# http://192.168.2.97:8000

# http://172.22.120.233:8000/docs#/
# my_fast_api