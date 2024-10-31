from fastapi import FastAPI
from dbtools import DBtool
from classes.table import Table
from classes.order import Order
from classes.item import Item
from enum import Enum
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from typing import Dict

class ModelName(str, Enum):
    description = "name"
    price = "price"
    category = "category"
    
class OrderNote(BaseModel):
    table: str
    order: Dict[str, int]
    

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
# dbtool = DBtool(host="mongodb://root:password@good-mongo")
dbtool = DBtool()
t = Table(dbtool)
o = Order(dbtool)
i = Item(dbtool)


# @app.get('/')
# async def index():
#     return {"status": 200, "msg": "Server is running :)"}


### TABLES ###
@app.get('/table/{table}')
async def tableInfo(request: Request, table: str):
    table_info = await t.getInfo(table)
    return templates.TemplateResponse("table-info.html", {"request": request, "table": table_info})


@app.get('/tables')
async def tables(request: Request):
    tables = await t.getInfoAll()
    return templates.TemplateResponse("tables.html", {"request": request, "tables": tables})


@app.post('/create-table')
async def create_table(table: str = Form()):
    await t.createTable(table)
    return RedirectResponse(f"/table/{table}", status_code=303)

# TODO change table values and discount function


@app.put('/pay-table')
async def pay_table(table: str):
    await t.pay(table)
    return {"status": f"Pay {table}"}


@app.delete('/delete-table')
async def delete_table(table: str):
    await t.delete(table)
    return {"status": f"Delete {table}"}


### ORDERS ###
@app.get('/')
async def get_active_orders(request: Request):
    orders = await o.getActiveOrders()
    # TODO if error
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})

@app.get('/orderinfo/{order}')
async def orderInfo(order: str):
    order_info = await o.getOrderInfo(order)
    return order_info

@app.get('/order')
async def order_page(request: Request):
    items = await i.getAllInfo()
    tables = await t.getInfoAll()
    return templates.TemplateResponse("order.html", {"request": request, "items": items, "tables": tables})

@app.post('/create-order')
async def create_order(data: OrderNote):
    order = data.dict()
    await o.createOrder(table=order['table'], order=order["order"])
    return RedirectResponse("/tables", status_code=303)


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
