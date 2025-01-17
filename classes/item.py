from dbtools import DBtool


class Item:
    def __init__(self, dbtool: DBtool):
        self.dbtool = dbtool
        self.database = "OrderAPI"
        self.collection = "Items"

    async def createItemList(self):
        await self.deleteAll()
        item_list = [
            {"code": "cafe", "name": "Cafe", "price": 1.60, "show": "false"},
            {"code": "cafe (soja)", "name": "Cafe (soja)", "price": 1.70, "show": "false"},
            {"code": "cafe (grande)", "name": "Cafe (grande)", "price": 1.70, "show": "false"},
            {"code": "cafe (llevar)", "name": "Cafe (llevar)", "price": 1.70, "show": "false"},
            {"code": "cafe (doble)", "name": "Cafe (doble)", "price": 2.00, "show": "false"},
            {"code": "churros", "name": "Churros", "price": 0.40, "show": "false"},
            {"code": "porras", "name": "Porras", "price": 0.80, "show": "false"},
            {"code": "tostada aceite", "name": "Tostada Aceite", "price": 1.70, "show": "false"},
            {"code": "tostada tomate", "name": "Tostada Tomate", "price": 1.70, "show": "false"},
            {"code": "tostada marmelada", "name": "Tostada Marmelada", "price": 1.70, "show": "false"},
            {"code": "tostada mixta", "name": "Tostada Mixta", "price": 3.50, "show": "false"},
            {"code": "tostada queso", "name": "Tostada Queso", "price": 3.50, "show": "false"},
            {"code": "tostada jamon", "name": "Tostada Jamon Serrano", "price": 3.50, "show": "false"},
            {"code": "tostada york", "name": "Tostada York", "price": 3.50, "show": "false"},
            {"code": "croissant", "name": "Croissant", "price": 1.70, "show": "false"},
            {"code": "croissant marmelada", "name": "Tostada Marmelada", "price": 1.70, "show": "false"},
            {"code": "croissant mixta", "name": "Croissant Mixta", "price": 3.50, "show": "false"},
            {"code": "croissant queso", "name": "Croissant Queso", "price": 3.50, "show": "false"},
            {"code": "croissant jamon", "name": "Croissant Jamon Serrano", "price": 3.50, "show": "false"},
            {"code": "croissant york", "name": "Croissant York", "price": 3.50, "show": "false"},
            {"code": "napolitana", "name": "Napolitana", "price": 1.70, "show": "false"},
            {"code": "infusion", "name": "Infusion", "price": 1.90, "show": "false"},
            {"code": "choco", "name": "Chocolate", "price": 2.50, "show": "false"},
            {"code": "choco peq.", "name": "Chocolate peq.", "price": 2.00, "show": "false"},
            {"code": "choco llevar", "name": "Chocolate (llevar)", "price": 2.60, "show": "false"},
            {"code": "choco medio", "name": "Chocolate 0.5L", "price": 6.00, "show": "false"},
            {"code": "choco litro", "name": "Chocolate 1L", "price": 12.00, "show": "false"},
            {"code": "vaso leche", "name": "Vaso de leche", "price": 1.60, "show": "true"},
            {"code": "zumo naranja", "name": "Zumo Naranja", "price": 3.00, "show": "true"},
            {"code": "zumo botella", "name": "Zumo Botellin", "price": 2.50, "show": "true"},
            {"code": "agua peq.", "name": "Agua peq.", "price": 1.50, "show": "true"},
            {"code": "agua grande", "name": "Agua grande", "price": 2.00, "show": "true"},
            {"code": "agua gas", "name": "Agua con gas", "price": 2.00, "show": "true"},
            {"code": "chupito", "name": "Chupito", "price": 1.50, "show": "true"},
            {"code": "licor", "name": "Licor", "price": 2.50, "show": "true"},
            {"code": "copa", "name": "Copa", "price": 5.00, "show": "true"},
            {"code": "refresco", "name": "Refresco", "price": 3.00, "show": "true"},
            {"code": "bolsa", "name": "Bolsa", "price": 0.10, "show": "true"}
        ]
        for item in item_list:
            await self.createItem(item['name'], item["code"], item["price"], item["show"])
        
    async def createItem(self, name: str, code: str, price: float, show: str):
        document = {"_id": code,
                    "name": name,
                    "price": price, 
                    "show": show}
        await self.dbtool.insertOne(self.database, self.collection, document)
        return document
    
    async def getOneInfo(self, code: str):
        document = await self.dbtool.findOne(self.database, self.collection, {"_id": code})
        return document
    
    async def getAllInfo(self, query: dict | None = {}):
        document = await self.dbtool.findAll(self.database, self.collection, 100, query)
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
        
    async def changeShow(self, code: str, show: str):
        await self.dbtool.updateOne(self.database, self.collection, {"_id": code}, {"show": show})
                
    async def delete(self, code: str):
        await self.dbtool.deleteOne(self.database, self.collection, {"_id": code})
        
    async def deleteAll(self):
        await self.dbtool.deleteMany(self.database, self.collection, {})
        