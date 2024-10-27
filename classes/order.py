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
        document = {"_id": table + "/" + str(count),
                    "table": table,
                    "status": "active",
                    "items": order}
        await self.dbtool.insertOne(self.database, self.collection, document)
        t = Table(self.dbtool)
        await t.addItems(table, order)
        return document
    
    async def getOrderInfo(self, order: str):
        document = await self.dbtool.findOne(self.database, self.collection, {"_id": order})
        return document
    
    async def getActiveOrders(self):
        document = await self.dbtool.findAll(self.database, self.collection, 100, {"status": "active"})
        return document
        
    async def cancelOrder(self, order: str):
        from .table import Table
        document = await self.dbtool.findOneValues(self.database, self.collection, {"_id": order}, ["items", "table"])
        order = document["items"]
        table = document["table"]
        t = Table(self.dbtool)
        await t.removeItems(table, order)
        await self.dbtool.updateOne(self.database, self.collection, {"_id": order}, {"status": "canceled"})
        
    async def completeOrder(self, order: str):
        await self.dbtool.updateOne(self.database, self.collection, {"_id": order}, {"status": "complete"})
       
    async def delete(self, order: str):
        await self.dbtool.deleteOne(self.database, self.collection, {"_id": order})
        
    async def deleteAll(self, table: str):
        await self.dbtool.deleteMany(self.database, self.collection, {"table": table})
        