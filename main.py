from fastapi import FastAPI
from dbtools import DBtool
from classes.table import Table
from classes.order import Order
from classes.item import Item
from enum import Enum
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse


class ModelName(str, Enum):
    description = "name"
    price = "price"
    category = "category"
    

app = FastAPI()
dbtool = DBtool()
t = Table(dbtool)
o = Order(dbtool)
i = Item(dbtool)


@app.get('/')
async def index():
    return {"status": 200, "msg": "Server is running :)"}


### TABLES ###
@app.get('/table/{table}')
async def tableInfo(table: str):
    table_info = await t.getInfo(table)
    return table_info


@app.get('/tables')
async def tables():
    l = await t.getInfoAll()
    return l


@app.post('/tables')
async def create_table(name: str):
    table = await t.createTable(name)
    return table

# TODO change table values and discount function


@app.put('/tables')
async def pay_table(table: str):
    await t.pay(table)
    return {"status": f"Pay {table}"}


@app.delete('/tables')
async def delete_table(table: str):
    await t.delete(table)
    return {"status": f"Delete {table}"}


### ORDERS ###
@app.get('/orders')
async def get_active_orders():
    l = await o.getActiveOrders()
    return l


@app.post('/')
async def create_order(table: str, order: dict):
    order = await o.createOrder(table=table, order=order)
    return order


@app.put('/orders')
async def complete_order(order: str):
    await o.completeOrder(order=order)
    return {"status": f"Complete {order}"}


@app.delete('/orders')
async def cancel_order(order: str):
    await o.cancelOrder(order=order)
    return {"status": f"Cancel {order}"}


### ITEMS ###
@app.post('/items')
async def create_item(name: str, code: str, price: float, category: str):
    item = await i.createItem(name=name, code=code, price=price, category=category)
    return item

@app.put('/items')
async def change_item(item: str, model_name: ModelName, value: float | str):
    if model_name is ModelName.description:
        await i.changeName(item, value)
    if model_name is ModelName.price:
        await i.changePrice(item, float(value))
    if model_name is ModelName.category:
        await i.changeCategory(item, value)
    return {"status": f"Change {item} {model_name.value} to {value}"}

@app.delete('/items')
async def delete_item(item: str):
    await i.delete(item)
    return {"status": f"Delete {item}"}
