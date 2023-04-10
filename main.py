from fastapi import FastAPI
from app.v01.routes.router import joke  

app = FastAPI()

#incluimos enrutador para chistes

app.include_router(joke)