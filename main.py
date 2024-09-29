from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Annotated
from fastapi import FastAPI, Query, Request, Response, Path
from fastapi.encoders import jsonable_encoder
import json 
from fastapi.responses import JSONResponse
import fastapi.logger as logger
import pydantic
from sqlalchemy.orm import defer
from dto import OrderDto, ProductDto, UpdateOrderStatus

from config import Engine, Session
from models import BaseModel, Product


@asynccontextmanager
async def lifespan(app: FastAPI):
    BaseModel.metadata.create_all(Engine)

    print("Starting the app...")
    yield
    BaseModel.metadata.drop_all(Engine)
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
def create_product(product: ProductDto):
    with Session() as s:
        s.add(Product(**product.model_dump()))
        s.commit()


@app.get("/products")
def get_products():
    with Session() as session:
        out = session.query(Product).options(defer(Product.id)).all()
        return out


@app.get("/products/{id}")
# pydantic will check if the mapping went well
def get_product(id: int, res: Response) -> ProductDto | None:
    with Session() as session:
        out: ProductDto | None = session.get(Product, id)
    if out:
        return out
    res.status_code = HTTPStatus.NOT_FOUND


@app.put("/products/{id}")
def update_product(id: int, req: Request, res: Response) -> None:
    # 200 or 201 or 204
    
    with Session() as session:
        out = session.query(Product).\
            filter(Product.id == id)
        if not out:
            res.status_code = HTTPStatus.NO_CONTENT
            return
        values = json.loads(req.body)
        dto = ProductDto(**values)
        out.update(dto)


@app.delete("/products/{id}")
def delete_product(id: int, res: Response) -> None:
    # 200 or 204
    with Session() as session:
        rows = session.query(Product).filter(Product.id == id).delete()
        if rows != 1:
            res.status_code = HTTPStatus.NO_CONTENT


# Orders

@app.post("/orders")
def create_order(order: OrderDto):
    # 201 or 204
    ...


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

    ...
