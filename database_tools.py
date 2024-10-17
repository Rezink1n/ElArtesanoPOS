from motor.motor_asyncio import AsyncIOMotorClient


async def insertOne(client: AsyncIOMotorClient, database: str, collection: str, document: dict):
    await client[database][collection].insert_one(document)
    
    
async def findOne(client: AsyncIOMotorClient, database: str, collection: str, query: dict):
    document = await client[database][collection].find_one(query)
    return document


async def findOneValue(client: AsyncIOMotorClient, database: str, collection: str, query: dict, key: str):
    document = await client[database][collection].find_one(query)
    try:
        return document[key]
    except:
        return None
    

async def findOneValues(client: AsyncIOMotorClient, database: str, collection: str, query: dict, keys: list):
    document = await client[database][collection].find_one(query)
    print(document)
    data = {}
    try:
        for item in keys:
            data[item] = document[item]
        return data
    except:
        return None

    
async def findAll(client: AsyncIOMotorClient, database: str, collection: str, leght: int):
    cursor = client[database][collection].find({})
    document = await cursor.to_list(leght)
    return document


async def updateOne(client: AsyncIOMotorClient, database: str, collection: str, query: dict, update: dict):
    result = await client[database][collection].update_one(query, {"$set": update})
    return True
    

async def deleteOne(client: AsyncIOMotorClient, database: str, collection: str, query: dict):
    await client[database][collection].delete_one(query)
    

async def deleteOneValues(client: AsyncIOMotorClient, database: str, collection: str, query: dict, keys: list):
    document = await client[database][collection].find_one(query)
    _id = document["_id"]
    for key in keys:
        document.pop(key, None)
    await client[database][collection].replace_one({"_id": _id}, document)


async def moveToDatabase(client: AsyncIOMotorClient, database: str, collection: str, query: dict, new_database: str, new_collection: str):
    document = await findOne(client, database, collection, query)
    await insertOne(client, new_database, new_collection, document)
    await deleteOne(client, database, collection, query)
    