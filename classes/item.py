from motor.motor_asyncio import AsyncIOMotorClient
import database_tools as dbt


class Item:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.database = "OrderAPI"
        self.collection = "Items"
        
    async def createItem(self, name: str, code: str, price: float, category: str):
        document = {"name": name,
                    "code": code,
                    "price": price,
                    "category": category}
        await dbt.insertOne(self.client, self.database, self.collection, document)
    
    async def getOneInfo(self, code: str):
        document = await dbt.findOne(self.client, self.database, self.collection, {"code": code})
        return document
    
    async def getAllInfo(self):
        document = await dbt.findAll(self.client, self.database, self.collection, {}, 100)
        return document
    
    async def getPriceDict(self):
        documents = await dbt.findAll(self.client, self.database, self.collection, {}, 100)
        price_dict = {}
        for document in documents:
            price_dict.update({document["code"]: document["price"]})
        return price_dict
        
    async def changeName(self, code: str, new_name: str):
        await dbt.updateOne(self.client, self.database, self.collection, {"code": code}, {"name": new_name})
        
    async def changeCode(self, code: str, new_code: str):
        await dbt.updateOne(self.client, self.database, self.collection, {"code": code}, {"code": new_code})
        
    async def changePrice(self, code: str, price: float):
        await dbt.updateOne(self.client, self.database, self.collection, {"code": code}, {"price": price})
        
    async def changeCategory(self, code: str, category: str):
        await dbt.updateOne(self.client, self.database, self.collection, {"code": code}, {"category": category})
       
    async def delete(self, code: str):
        await dbt.deleteOne(self.client, self.database, self.collection, {"code": code})
        