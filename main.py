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
    place = "place"
    
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
    items = table_info["items"]
    return templates.TemplateResponse("table-info.html", {"request": request, "table": table_info, "items": items})


@app.get('/tables')
async def tables(request: Request):
    tables = await t.getInfoAll()
    return templates.TemplateResponse("tables.html", {"request": request, "tables": tables})


@app.post('/create-table')
async def create_table(table: str = Form()):
    await t.createTable(table)
    return RedirectResponse(f"/table/{table}", status_code=303)

# TODO change table values and discount function


@app.post('/table/pay-table')
async def pay_table(table: str = Form()):
    await t.pay(table)
    return RedirectResponse("/", status_code=303)


@app.post('/table/delete-table')
async def delete_table(table: str = Form()):
    await t.delete(table)
    return RedirectResponse("/", status_code=303)


### ORDERS ###
@app.get('/')
async def get_active_orders(request: Request):
    orders = await o.getActiveOrders()
    # TODO if error
    items: dict = {}
    for order in orders:
        item = order["items"]
        items[order["_id"]] = item
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders, "items": items})

# @app.get('/orders')
# async def get_active_orders(request: Request):
#     orders = await o.getActiveOrders()
#     items: dict = {}
#     for order in orders:
#         item = order["items"]
#         items[order["_id"]] = item
#     return templates.TemplateResponse("orders.html", {"request": request, "orders": orders, "items": items})

@app.get('/order-info/{order}')
async def orderInfo(request: Request, order: str):
    order_info = await o.getOrderInfo(order)
    items = order_info["items"]
    return templates.TemplateResponse("order-info.html", {"request": request, "order": order_info, "items": items})

@app.get('/order')
async def order_page(request: Request, table: str | None = "Choose the table"):
    items = await i.getAllInfo()
    tables = await t.getInfoAll()
    holder = table
    return templates.TemplateResponse("order.html", {"request": request, "items": items, "tables": tables, "holder": holder})

@app.post('/create-order')
async def create_order(data: OrderNote):
    order = data.dict()
    await o.createOrder(table=order['table'], order=order["order"])
    return RedirectResponse("/", status_code=303)


@app.post('/complete-order')
async def complete_order(order: str = Form()):
    await o.completeOrder(order=order)
    return RedirectResponse("/", status_code=303)


@app.post('/order-info/cancel-order')
async def cancel_order(order: str = Form()):
    await o.cancelOrder(order=order)
    return RedirectResponse("/", status_code=303)


### ITEMS ###
@app.get('/item/{item}')
async def itemInfo(request: Request, item: str):
    item_info = await i.getOneInfo(item)
    return templates.TemplateResponse("item-info.html", {"request": request, "item": item_info})


@app.get('/items')
async def items(request: Request):
    items = await i.getAllInfo()
    return templates.TemplateResponse("items.html", {"request": request, "items": items})


@app.post('/create-item')
async def create_item(name: str = Form(), code: str = Form(), price: str = Form(), place: int = Form()):
    await i.createItem(name=name, code=code, price=float(price), place=place)
    return RedirectResponse("/items", status_code=303)


@app.post('/item/change-item')
async def change_item(item: str = Form(), model_name: ModelName = Form(), value: str = Form()):
    if model_name is ModelName.description:
        await i.changeName(item, value)
    if model_name is ModelName.price:
        await i.changePrice(item, float(value))
    if model_name is ModelName.place:
        await i.changePlace(item, int(value))
    return RedirectResponse("/items", status_code=303)

@app.post('/item/delete-item')
async def delete_item(item: str = Form()):
    await i.delete(item)
    return RedirectResponse("/items", status_code=303)
