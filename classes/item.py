from dbtools import DBtool


class Item:
    def __init__(self, dbtool: DBtool):
        self.dbtool = dbtool
        self.database = "OrderAPI"
        self.collection = "Items"
        
    async def createItem(self, name: str, code: str, price: float, category: str):
        document = {"_id": code,
                    "name": name,
                    "price": price,
                    "category": category}
        await self.dbtool.insertOne(self.database, self.collection, document)
        return document
    
    async def getOneInfo(self, code: str):
        document = await self.dbtool.findOne(self.database, self.collection, {"_id": code})
        return document
    
    async def getAllInfo(self):
        document = await self.dbtool.findAll(self.database, self.collection, 100)
        return document
    
    async def getPriceDict(self):
        documents = await self.dbtool.findAll(self.database, self.collection, 100)
        price_dict = {}
        for document in documents:
            price_dict.update({document["_id"]: document["price"]})
        return price_dict
        
    async def changeName(self, code: str, new_name: str):
        await self.dbtool.updateOne(self.database, self.collection, {"_id": code}, {"name": new_name})
                
    async def changePrice(self, code: str, price: float):
        await self.dbtool.updateOne(self.database, self.collection, {"_id": code}, {"price": price})
        
    async def changeCategory(self, code: str, category: str):
        await self.dbtool.updateOne(self.database, self.collection, {"_id": code}, {"category": category})
       
    async def delete(self, code: str):
        await self.dbtool.deleteOne(self.database, self.collection, {"_id": code})
        