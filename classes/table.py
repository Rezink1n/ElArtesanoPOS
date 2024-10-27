from dbtools import DBtool 
from .item import Item


class Table:
    def __init__(self, dbtool: DBtool):
        self.dbtool = dbtool
        self.database = "OrderAPI"
        self.collection = "Tables"
    
    async def createTable(self, name: str):
        duplicate = await self.dbtool.countDocuments(self.database, self.collection, {"name": name})
        if duplicate > 0:
            table = name + "/" + str(duplicate)
        else:
            table = name
        document = {"table": table,
                    "name": name,
                    "duplicate": duplicate,
                    "status": "active",
                    "bill": 0,
                    "items": {}}
        await self.dbtool.insertOne(self.database, self.collection, document)
    
    async def getInfo(self, name: str):
        document = await self.dbtool.findOne(self.database, self.collection, {"name": name})
        return document
        
    async def changeName(self, name: str, new_name: str):
        await self.dbtool.updateOne(self.database, self.collection, {"name": name}, {"name": new_name})
         
    async def addItems(self, name: str, order: dict):
        items: dict = await self.dbtool.findOneValue(self.database, self.collection, {"name": name}, "items")
        for item in order:
            existance = items.get(item)
            if existance is None:
                items.update({item: order[item]})
            else:
                existance += order[item]
                items.update({item: existance})
        await self.dbtool.updateOne(self.database, self.collection, {"name": name}, {"items": items})
        i = Item(self.dbtool)
        pd = await i.getPriceDict()
        bill = 0
        for item in items:
            bill += (items[item] * pd[item])
        await self.dbtool.updateOne(self.database, self.collection, {"name": name}, {"bill": bill})
                
    async def removeItems(self, name: str, order: dict):
        document: dict = await self.dbtool.findOneValues(self.database, self.collection, {"name": name}, ["items", "bill"])
        items = document["items"]
        for item in order:
            items[item] = items[item] - order[item]
            if items[item] == 0:
                items.pop({item})
        await self.dbtool.updateOne(self.database, self.collection, {"name": name}, {"items": items})
        i = Item(self.dbtool)
        pd = await i.getPriceDict()
        bill = document["bill"]
        for item in order:
            bill -= (order[item] * pd[item])
        await self.dbtool.updateOne(self.database, self.collection, {"name": name}, {"bill": bill})
        
    async def updateItems(self, name: str, updated_items: dict):
        await self.dbtool.updateOne(self.database, self.collection, {"name": name}, {"items": updated_items})
        
    async def pay(self, name: str):
        await self.dbtool.updateOne(self.database, self.collection, {"name": name}, {"status": "paid"})
        await self.dbtool.moveToDatabase(self.database, self.collection, {"name": name}, self.database, "Bills")
        
    async def discountBill(self, name: str, discount: float):
        bill = await self.dbtool.findOneValue(self.database, self.collection, {"name": name}, "bill")
        bill -= discount
        await self.dbtool.updateOne(self.database, self.collection, {"name": name}, {"bill": bill})
       
    async def delete(self, name: str):
        await self.dbtool.deleteOne(self.database, self.collection, {"name": name})
        