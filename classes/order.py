from dbtools import DBtool


class Order:
    def __init__(self, dbtool: DBtool):
        self.dbtool = dbtool
        self.database = "OrderAPI"
        self.collection = "Orders"
    
    async def createOrder(self, table: str, order: dict):
        from .table import Table 
        counts = await self.dbtool.countDocuments(self.database, self.collection, {"table": table})
        count = counts
        document = {"name": table + "/" + str(count),
                    "table": table,
                    "status": "active",
                    "items": order}
        await self.dbtool.insertOne(self.database, self.collection, document)
        t = Table(self.dbtool)
        await t.addItems(table, order)
    
    async def getInfo(self):
        document = await self.dbtool.findAll(self.database, self.collection, 100, {"status": "active"})
        return document
        
    async def cancelOrder(self, name: str):
        from .table import Table
        document = await self.dbtool.findOneValues(self.database, self.collection, {"name": name}, ["items", "table"])
        order = document["items"]
        table = document["table"]
        t = Table(self.dbtool)
        await t.removeItems(table, order)
        await self.dbtool.updateOne(self.database, self.collection, {"name": name}, {"status": "canceled"})
        
    async def completeOrder(self, name: str):
        await self.dbtool.updateOne(self.database, self.collection, {"name": name}, {"status": "complete"})
       
    async def delete(self, name: str):
        await self.dbtool.deleteOne(self.database, self.collection, {"name": name})
        
    async def deleteAll(self, table: str):
        await self.dbtool.deleteMany(self.database, self.collection, {"table": table})
        