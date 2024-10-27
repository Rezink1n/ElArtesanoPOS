from dbtools import DBtool 


class Table:
    def __init__(self, dbtool: DBtool):
        self.dbtool = dbtool
        self.database = "OrderAPI"
        self.collection = "Tables"
    
    async def createTable(self, name: str):
        duplicate = await self.dbtool.countDocuments(self.database, self.collection, {"name": name})
        if duplicate > 0:
            table = name + "-" + str(duplicate)
        else:
            table = name
        document = {"_id": table,
                    "name": name,
                    "duplicate": duplicate,
                    "status": "active",
                    "bill": 0,
                    "items": {}}
        await self.dbtool.insertOne(self.database, self.collection, document)
        return document
    
    async def getInfo(self, table: str):
        document = await self.dbtool.findOne(self.database, self.collection, {"_id": table})
        return document
    
    async def getInfoAll(self):
        document = await self.dbtool.findAll(self.database, self.collection, 100)
        return document
        
    async def changeName(self, name: str, new_name: str):
        await self.dbtool.updateOne(self.database, self.collection, {"name": name}, {"name": new_name})
         
    async def addItems(self, table: str, order: dict):
        from .item import Item
        items: dict = await self.dbtool.findOneValue(self.database, self.collection, {"_id": table}, "items")
        for item in order:
            existance = items.get(item)
            if existance is None:
                items.update({item: order[item]})
            else:
                existance += order[item]
                items.update({item: existance})
        await self.dbtool.updateOne(self.database, self.collection, {"_id": table}, {"items": items})
        i = Item(self.dbtool)
        pd = await i.getPriceDict()
        bill = 0
        for item in items:
            bill += (items[item] * pd[item])
        await self.dbtool.updateOne(self.database, self.collection, {"_id": table}, {"bill": bill})
                
    async def removeItems(self, table: str, order: dict):
        from .item import Item
        document: dict = await self.dbtool.findOneValues(self.database, self.collection, {"_id": table}, ["items", "bill"])
        items = document["items"]
        for item in order:
            items[item] = items[item] - order[item]
            if items[item] == 0:
                items.pop(item)
        await self.dbtool.updateOne(self.database, self.collection, {"_id": table}, {"items": items})
        i = Item(self.dbtool)
        pd = await i.getPriceDict()
        bill = document["bill"]
        for item in order:
            bill -= (order[item] * pd[item])
        await self.dbtool.updateOne(self.database, self.collection, {"_id": table}, {"bill": bill})
        
    async def updateItems(self, table: str, updated_items: dict):
        await self.dbtool.updateOne(self.database, self.collection, {"_id": table}, {"items": updated_items})
        
    async def pay(self, table: str):
        from .order import Order
        await self.dbtool.updateOne(self.database, self.collection, {"_id": table}, {"status": "paid"})
        await self.dbtool.moveToDatabase(self.database, self.collection, {"_id": table}, self.database, "Bills")  
        # TODO fix the save conflict of same ID in "Bills"
        o = Order(self.dbtool)
        await o.deleteAll(table)
        
    async def discountBill(self, table: str, discount: float):
        bill = await self.dbtool.findOneValue(self.database, self.collection, {"_id": table}, "bill")
        bill -= discount
        await self.dbtool.updateOne(self.database, self.collection, {"_id": table}, {"bill": bill})
       
    async def delete(self, table: str):
        from .order import Order
        await self.dbtool.deleteOne(self.database, self.collection, {"_id": table})
        o = Order(self.dbtool)
        await o.deleteAll(table)
   