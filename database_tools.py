from motor.motor_asyncio import AsyncIOMotorClient


async def insertOne(client: AsyncIOMotorClient, database: str, collection: str, document: dict):
    """Create a document
    Args:
        client (AsyncIOMotorClient): Motor client
        database (str): name of database
        collection (str): name of collection
        document (dict): data to upload on database
    """
    await client[database][collection].insert_one(document)
    
    
async def findOne(client: AsyncIOMotorClient, database: str, collection: str, query: dict):
    """Get whole data from the document
    Args:
        client (AsyncIOMotorClient): Motor client
        database (str): name of database
        collection (str): name of collection
        query (dict): document search request, like {"Name": "John"}

    Returns:
        dict: {"some": "data"}
    """
    document = await client[database][collection].find_one(query)
    return document


async def findOneValue(client: AsyncIOMotorClient, database: str, collection: str, query: dict, key: str):
    """Get a value from the document
    Args:
        client (AsyncIOMotorClient): Motor client
        database (str): name of database
        collection (str): name of collection
        query (dict): document search request, like {"Name": "John"}
        key (str): the search value, for example "Age"

    Returns:
        Any : returns the value
        None : if it's not found
    """
    document = await client[database][collection].find_one(query)
    try:
        return document[key]
    except:
        return None
    

async def findOneValues(client: AsyncIOMotorClient, database: str, collection: str, query: dict, keys: list):
    """Get multiple values from the document
    Args:
        client (AsyncIOMotorClient): Motor client
        database (str): name of database
        collection (str): name of collection
        query (dict): document search request, like {"Name": "John"}
        keys (list): strings of multiple search values, for example ["Age", "Sex", "Phone"]

    Returns:
        dict : values {"Age": 18, "Sex": male, ...}
        None : if it's not found
    """
    document = await client[database][collection].find_one(query)
    print(document)
    data = {}
    try:
        for item in keys:
            data[item] = document[item]
        return data
    except:
        return None

    
async def findAll(client: AsyncIOMotorClient, database: str, collection: str, query: dict, leght: int):  # TODO update DOCS 'cuz "query"
    """Get a list of multiple documents from entire database's collection
    Args:
        client (AsyncIOMotorClient): Motor client
        database (str): name of database
        collection (str): name of collection
        leght (int): amount of documents

    Returns:
        list: list of documents
    """
    cursor = client[database][collection].find(query)
    documents_list = await cursor.to_list(leght)
    return documents_list


async def updateOne(client: AsyncIOMotorClient, database: str, collection: str, query: dict, update: dict):
    """Update a value in the document
    Args:
        client (AsyncIOMotorClient): Motor client
        database (str): name of database
        collection (str): name of collection
        query (dict): document search request, like {"Name": "John"}
        update (dict): new value, for example {"Name": "Johnny"}
    """
    result = await client[database][collection].update_one(query, {"$set": update})
    

async def deleteOne(client: AsyncIOMotorClient, database: str, collection: str, query: dict):
    """Delete a document from the collection
    Args:
        client (AsyncIOMotorClient): Motor client
        database (str): name of database
        collection (str): name of collection
        query (dict): document search request, like {"Name": "John"}
    """
    await client[database][collection].delete_one(query)
    

async def deleteOneValues(client: AsyncIOMotorClient, database: str, collection: str, query: dict, keys: list):
    """Delete values from the document
    Args:
        client (AsyncIOMotorClient): Motor client
        database (str): name of database
        collection (str): name of collection
        query (dict): document search request, like {"Name": "John"}
        keys (list): list of one or more values to delete, ["Phone", "Email", ...]
    """
    document = await client[database][collection].find_one(query)
    _id = document["_id"]
    for key in keys:
        document.pop(key, None)
    await client[database][collection].replace_one({"_id": _id}, document)


async def moveToDatabase(client: AsyncIOMotorClient, database: str, collection: str, query: dict, new_database: str, new_collection: str):
    """Move a document from one database to another one
    Args:
        client (AsyncIOMotorClient): Motor client
        database (str): name of database
        collection (str): name of collection
        query (dict): document search request, like {"Name": "John"}
        new_database (str): new destination
        new_collection (str): new destination
    """
    document = await findOne(client, database, collection, query)
    await insertOne(client, new_database, new_collection, document)
    await deleteOne(client, database, collection, query)
    
    
async def countDocuments(client: AsyncIOMotorClient, database: str, collection: str, query: dict):
    """Count amount of documents in collection
    Args:
        client (AsyncIOMotorClient): Motor client
        database (str): name of database
        collection (str): name of collection
        query (dict): document search request, like {"status": "active"}

    Returns:
        int : amount
    """
    count = await client[database][collection].count_documents(query)
    return count