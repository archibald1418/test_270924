import itertools
import json
from contextlib import asynccontextmanager
from http import HTTPStatus
from pprint import pprint
from typing import Annotated, Any, Dict, cast

import fastapi.logger as logger
from fastapi import FastAPI, HTTPException, Path, Query, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import delete, select, text, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import defer

from config import Session
from dto import CreateOrderDto, OrderDto, ProductDto, UpdateOrderStatus
from models import Order, OrderItem, Product


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting the app...")
    yield
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
        raise HTTPException(status_code=HTTPStatus.CONFLICT,
                            detail="The product is already present")


@app.get("/products")
def get_products() -> list[ProductDto]:
    with Session() as session:
        stmt = select(Product)
        out = session.execute(stmt).fetchall()
        return list(*out)


@app.get("/products/{id}")
# pydantic will check if the mapping went well
def get_product(id: str) -> ProductDto | None:
    with Session() as session:
        stmt = select(Product).where(Product.id == id)
        if (out := session.execute(stmt).first()):
            return out[0]
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                        detail='Product not found')


@app.put("/products/{id}", response_model=None, status_code=HTTPStatus.NO_CONTENT)
def update_product(id: str, productUpdate: ProductDto):
    with Session() as session:
        stmt = update(Product)\
            .where(Product.id == id)\
            .values(**productUpdate.model_dump())
        if not session.execute(stmt).rowcount:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Product not found')
        session.commit()


@app.delete("/products/{id}", status_code=HTTPStatus.NO_CONTENT)
def delete_product(id: str) -> None:
    with Session() as session:
        stmt = delete(Product).where(Product.id == id)
        if not session.execute(stmt).rowcount:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Product not found')
        session.commit()


# Orders

@app.post("/orders", status_code=HTTPStatus.CREATED)
def create_order(newOrder: CreateOrderDto) -> None:
    # 201 or 409
    with Session() as s:
        product: Product | None = s.get(Product, newOrder.product_id)
        if not product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Product not found')
        if product.amount_in_stock < newOrder.amount:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                                detail='Not enough product in stock')

        product.amount_in_stock -= newOrder.amount

        o = Order()
        s.add(o)
        s.flush()  # send without commiting, updating the current context - making the id available straight away

        newOrderItem = OrderItem(
            product_id=product.id, order_id=o.id, amount=newOrder.amount)
        s.add(newOrderItem)
        s.commit()


@app.get("/orders")
def get_orders() -> list[OrderDto]:
    with Session() as session:
        stmt = select(Order)
        out = session.execute(stmt).fetchall()
        pprint(out)
        return list(itertools.chain(*out))


@app.get("/orders/{id}")
def get_order(id: str) -> OrderDto:
    with Session() as session:
        stmt = select(Order).where(Order.id == id)
        if (out := session.execute(stmt).first()):
            return out[0]
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                        detail='Order not found')


@app.patch("/orders/{id}/status", status_code=HTTPStatus.NO_CONTENT)
def update_order_status(id: str, orderStatus: UpdateOrderStatus):
    with Session() as session:
        stmt = update(Order)\
            .where(Order.id == id)\
            .values(**orderStatus.model_dump())
        if not session.execute(stmt).rowcount:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Order not found')
        session.commit()


if __name__ == "__main__":
    ...
    '''For testing purposes'''
    # try:
    #     uvicorn.run("main:app", workers=1, reload=True)
    # except Exception as e:
    #     print(e)
    #     print("Leaving")
