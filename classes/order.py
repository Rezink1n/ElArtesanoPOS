from motor.motor_asyncio import AsyncIOMotorClient
import database_tools as dbt
from .table import Table


class Order:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.database = "OrderAPI"
        self.collection = "Orders"
    
    async def createOrder(self, table: str, order: dict):
        count = 1  #TODO Create a count change, like #1/1, #1/2, Table 1/3 .
        document = {"name": table + "/" + str(count),
                    "table": table,
                    "status": "active",
                    "items": order}
        await dbt.insertOne(self.client, self.database, self.collection, document)
        t = Table(self.client)
        await t.addItems(table, order)
    
    async def getInfo(self):
        document = await dbt.findAll(self.client, self.database, self.collection, {"status": "active"}, 100)
        return document
        
    async def undoLastOrder(self, name: str, table: str):
        #TODO ??? delete items from table as well, to remove N quantity of items from table
        pass
    
    async def completeOrder(self, name: str, table: str):
        await dbt.updateOne(self.client, self.database, self.collection, {"name": name}, {"status": "complete"})
        # await self.delete(name)  #TODO delete order after complete??
       
    async def delete(self, name: str):
        await dbt.deleteOne(self.client, self.database, self.collection, {"name": name})
        