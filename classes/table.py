from motor.motor_asyncio import AsyncIOMotorClient
import database_tools as dbt
from .item import Item


class Table:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.database = "OrderAPI"
        self.collection = "Tables"
    
    async def createTable(self, name: str):
        duplicate = await dbt.countDocuments(self.client, self.database, self.collection, {"name": name})
        if duplicate > 0:
            idn = name + "/" + str(duplicate)
        else:
            idn = name
        document = {"idn": idn,  # TODO change idn name
                    "name": name,
                    "duplicate": duplicate,
                    "status": "active",
                    "bill": 0,
                    "items": {}}
        await dbt.insertOne(self.client, self.database, self.collection, document)
    
    async def getInfo(self, name: str):
        document = await dbt.findOne(self.client, self.database, self.collection, {"name": name})
        return document
        
    async def changeName(self, name: str, new_name: str):
        await dbt.updateOne(self.client, self.database, self.collection, {"name": name}, {"name": new_name})
         
    async def addItems(self, name: str, order: dict):
        items: dict = await dbt.findOneValue(self.client, self.database, self.collection, {"name": name}, "items")
        for item in order:
            existance = items.get(item)
            if existance is None:
                items.update({item: order[item]})
            else:
                existance += order[item]
                items.update({item: existance})
        await dbt.updateOne(self.client, self.database, self.collection, {"name": name}, {"items": items})
        i = Item(self.client)
        pd = await i.getPriceDict()
        bill = 0
        for item in items:
            bill += (items[item] * pd[item])
        await dbt.updateOne(self.client, self.database, self.collection, {"name": name}, {"bill": bill})
                
    async def removeItems(self, name: str, order: dict):
        document: dict = await dbt.findOneValues(self.client, self.database, self.collection, {"name": name}, ["items", "bill"])
        items = document["items"]
        for item in order:
            items[item] = items[item] - order[item]
            if items[item] == 0:
                items.pop({item})
        await dbt.updateOne(self.client, self.database, self.collection, {"name": name}, {"items": items})
        i = Item(self.client)
        pd = await i.getPriceDict()
        bill = document["bill"]
        for item in order:
            bill -= (order[item] * pd[item])
        await dbt.updateOne(self.client, self.database, self.collection, {"name": name}, {"bill": bill})
        
    async def updateItems(self, name: str, updated_items: dict):
        await dbt.updateOne(self.client, self.database, self.collection, {"name": name}, {"items": updated_items})
        
    async def pay(self, name: str):
        await dbt.updateOne(self.client, self.database, self.collection, {"name": name}, {"status": "paid"})
        await dbt.moveToDatabase(self.client, self.database, self.collection, {"name": name}, self.database, "Bills")
        
    async def discountBill(self, name: str, discount: float):
        bill = await dbt.findOneValue(self.client, self.database, self.collection, {"name": name}, "bill")
        bill -= discount
        await dbt.updateOne(self.client, self.database, self.collection, {"name": name}, {"bill": bill})
       
    async def delete(self, name: str):
        await dbt.deleteOne(self.client, self.database, self.collection, {"name": name})
        