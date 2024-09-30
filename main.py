from contextlib import asynccontextmanager
import uvicorn
from http import HTTPStatus
from pprint import pprint
from typing import Annotated, Dict, Any, cast
from fastapi import FastAPI, Query, Request, Response, Path
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
import json 
from fastapi.responses import JSONResponse
import fastapi.logger as logger
import pydantic
from sqlalchemy.orm import defer
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from dto import OrderDto, ProductDto, UpdateOrderStatus

from config import Engine, Session
from models import BaseModel, Order, Product

from pydantic import UUID4


@asynccontextmanager
async def lifespan(app: FastAPI):
    BaseModel.metadata.create_all(Engine)

    print("Starting the app...")
    yield
    # BaseModel.metadata.drop_all(Engine)
    print("Closing the app")


app = FastAPI(debug=True, title="This is a title",
              summary="This is a summary", lifespan=lifespan)


@app.get("/")
def root():
    return JSONResponse({
        "Hello": "This is App"
    })


# Produtc endpoints

@app.post("/products", status_code=HTTPStatus.CREATED)
def create_product(product: ProductDto, res: Response):
    try:
        with Session() as s:
            s.add(Product(**product.model_dump()))
            s.commit()
    except IntegrityError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="The product is already present")
        


@app.get("/products")
def get_products():
    with Session() as session:
        return session.query(Product).all()


@app.get("/products/{id}")
# pydantic will check if the mapping went well
def get_product(id: str) -> ProductDto | None:
    with Session() as session:
        stmt = select(Product).where(Product.id == id)
        if (out := session.execute(stmt).first()):
            return out[0]
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Product not found')


@app.put("/products/{id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def update_product(id: str, productUpdate: ProductDto):
    # 200 or 201 or 204
    with Session() as session:
        # stmt = select(Product).where(Product.id == id)
        stmt = update(Product)\
            .where(Product.id == id)\
            .values(**productUpdate.model_dump())
        if not session.execute(stmt).rowcount:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Product not found')
        session.commit()


@app.delete("/products/{id}", status_code=HTTPStatus.NO_CONTENT)
def delete_product(id: str) -> None:
    # 200 or 204
    # raise Exception("LOL")
    with Session() as session:
        stmt = delete(Product).where(Product.id == id)
        if not session.execute(stmt).rowcount:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Product not found')
        session.commit()


# Orders

@app.post("/orders")
def create_order(order: OrderDto):
    # 201 or 204
    try:
        with Session() as s:
            s.add(Order(**order.model_dump()))
            s.commit()
    except IntegrityError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="The order is already present")


@app.get("/orders")
def get_orders():
    ...


@app.get("/orders/{id}")
def get_order(id: int):
    ...


@app.patch("/orders{id}/status")
def update_order_status(id: int, orderStatus: UpdateOrderStatus, req: Request, res: Response):
    # 200 or 204
    # If no product - 204
    json_dict = json.loads(req.body)
    product = OrderDto(**json_dict)
    ...

# @app.get


if __name__ == "__main__":
    '''For testing purposes'''
    try:
        uvicorn.run("main:app", workers=1, reload=True)
    except Exception as e:
        print(e)
        print("Leaving")
