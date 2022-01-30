"""
uvicorn app:app --reload
http://localhost:8000/
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
"""

from tkinter import X
from typing import ItemsView, Optional
from fastapi import FastAPI
from backend import num_to_json

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from pydantic import BaseModel

import json

class Item(BaseModel):
    num_oc: int
    order_desc: Optional[str] = None


json_path = ['./out/df_oc.json', './out/df_1er.json']

app = FastAPI()

@app.get("/")
def index():
    return {"Info OC -->":"/data"}


@app.post("/data")
def data_item2(item:Item):
    data = num_to_json().filtrar(nro_oc=item.num_oc , json_path=['./out/df_oc.json', './out/df_1er.json'])
    json_compatible_item_data = jsonable_encoder(data)
    return JSONResponse(json_compatible_item_data)