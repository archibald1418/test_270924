import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, Path
from fastapi.responses import JSONResponse
import fastapi.logger as logger
import pydantic
from dto import OrderDto, OrderStatusDto, ProductDto


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
        "Hello" : "This is App"
    })


# Produtc endpoints

@app.post("/products")
def create_product(proudct: ProductDto):
    ...

@app.get("/products")
def get_products():
    ...

@app.get("/products/{id}")
def get_product(id: int): # TODO: id format
    ...

@app.put("/products/{id}")
def update_product(id: int, product: ProductDto):
    ...

@app.delete("/products/{id}")
def delete_product(id: int):
    ...


# Orders

@app.post("/orders")
def create_order(order: OrderDto):
    ...


@app.get("/orders")
def get_orders():
    ...

@app.get("/orders/{id}")
def get_order(id: int):
    ...

@app.patch("/orders{id}/status")
def update_order_status(id: int, orderStatus: OrderStatusDto):
    ...

# @app.get


# '''
# Реализация REST API:
# Эндпоинты для товаров:
# Создание товара (POST /products).
# Получение списка товаров (GET /products).
# Получение информации о товаре по id (GET /products/{id}).
# Обновление информации о товаре (PUT /products/{id}).
# Удаление товара (DELETE /products/{id}).
# Эндпоинты для заказов:
# Создание заказа (POST /orders).
# Получение списка заказов (GET /orders).
# Получение информации о заказе по id (GET /orders/{id}).
# Обновление статуса заказа (PATCH /orders/{id}/status).
# '''


if __name__ == "__main__":
    '''For testing purposes'''

    ...
