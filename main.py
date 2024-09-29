from contextlib import asynccontextmanager
from http import HTTPStatus
from fastapi import FastAPI, Request, Response, Path
from fastapi.responses import JSONResponse
import fastapi.logger as logger
import pydantic
from sqlalchemy import MetaData
from dto import OrderDto, OrderStatusDto, ProductDto

from config import Engine, Session
from models import BaseModel, Product

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
        "Hello" : "This is App"
    })


# Produtc endpoints

@app.post("/products", status_code=HTTPStatus.CREATED)
def create_product(proudct: ProductDto):
    ...

@app.get("/products")
def get_products():
    with Session() as session:
        return session.query(Product).all()

@app.get("/products/{id}")
def get_product(id: int, res: Response) -> ProductDto | None:
    with Session() as session:
        out: ProductDto | None = session.get(Product, id)
    if out:
        return out
    res.status_code = HTTPStatus.NOT_FOUND


@app.put("/products/{id}")
def update_product(id: int, product: ProductDto):
    # 200 or 201 or 204
    ...

@app.delete("/products/{id}")
def delete_product(id: int):
    # 200 or 204
    ...


# Orders

@app.post("/orders")
def create_order(order: OrderDto):
    # 200 or 204
    ...


@app.get("/orders")
def get_orders():
    ...

@app.get("/orders/{id}")
def get_order(id: int):
    ...

@app.patch("/orders{id}/status")
def update_order_status(id: int, orderStatus: OrderStatusDto):
    # 200 or 204
    ...

# @app.get


if __name__ == "__main__":
    '''For testing purposes'''

    ...
