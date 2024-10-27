from motor.motor_asyncio import AsyncIOMotorClient


class DBtool:
    def __init__(self, host: str | None = "localhost", port: int | None = 27017):
        self.client = AsyncIOMotorClient(host, port)


    async def insertOne(self, database: str, collection: str, document: dict):
        """Create a document
        Args:    
            database (str): name of database
            collection (str): name of collection
            document (dict): data to upload on database
        """
        await self.client[database][collection].insert_one(document)
        
        
    async def findOne(self, database: str, collection: str, query: dict):
        """Get whole data from the document
        Args:   
            database (str): name of database
            collection (str): name of collection
            query (dict): document search request, like {"Name": "John"}

        Returns:
            dict: {"some": "data"}
        """
        document = await self.client[database][collection].find_one(query)
        return document


    async def findOneValue(self, database: str, collection: str, query: dict, key: str):
        """Get a value from the document
        Args:    
            database (str): name of database
            collection (str): name of collection
            query (dict): document search request, like {"Name": "John"}
            key (str): the search value, for example "Age"

        Returns:
            Any : returns the value
            None : if it's not found
        """
        document = await self.client[database][collection].find_one(query)
        try:
            return document[key]
        except:
            return None
        

    async def findOneValues(self, database: str, collection: str, query: dict, keys: list):
        """Get multiple values from the document
        Args: 
            database (str): name of database
            collection (str): name of collection
            query (dict): document search request, like {"Name": "John"}
            keys (list): strings of multiple search values, for example ["Age", "Sex", "Phone"]

        Returns:
            dict : values {"Age": 18, "Sex": male, ...}
            None : if it's not found
        """
        document = await self.client[database][collection].find_one(query)
        data = {}
        try:
            for item in keys:
                data[item] = document[item]
            return data
        except:
            return None

        
    async def findAll(self, database: str, collection: str, leght: int, query: dict | None = {}):
        """Get a list of multiple documents from entire database's collection
        Args: 
            database (str): name of database
            collection (str): name of collection
            leght (int): amount of documents
            query (dict | None = {}): get all documents by default
            
        Returns:
            list: list of documents
        """
        cursor = self.client[database][collection].find(query)
        documents_list = await cursor.to_list(leght)
        return documents_list


    async def updateOne(self, database: str, collection: str, query: dict, update: dict):
        """Update a value in the document
        Args: 
            database (str): name of database
            collection (str): name of collection
            query (dict): document search request, like {"Name": "John"}
            update (dict): new value, for example {"Name": "Johnny"}
        """
        await self.client[database][collection].update_one(query, {"$set": update})
        

    async def deleteOne(self, database: str, collection: str, query: dict):
        """Delete a document from the collection
        Args:
            database (str): name of database
            collection (str): name of collection
            query (dict): document search request, like {"Name": "John"}
        """
        await self.client[database][collection].delete_one(query)
        
        
    async def deleteMany(self, database: str, collection: str, query: dict):
        """Delete documents from the collection
        Args:
            database (str): name of database
            collection (str): name of collection
            query (dict): document search request, like {"Name": "John"}
        """
        await self.client[database][collection].delete_many(query)
        

    async def deleteOneValues(self, database: str, collection: str, query: dict, keys: list):
        """Delete values from the document
        Args:
            database (str): name of database
            collection (str): name of collection
            query (dict): document search request, like {"Name": "John"}
            keys (list): list of one or more values to delete, ["Phone", "Email", ...]
        """
        document = await self.client[database][collection].find_one(query)
        _id = document["_id"]
        for key in keys:
            document.pop(key, None)
        await self.client[database][collection].replace_one({"_id": _id}, document)


    async def moveToDatabase(self, database: str, collection: str, query: dict, new_database: str, new_collection: str):
        """Move a document from one database to another one
        Args:
            database (str): name of database
            collection (str): name of collection
            query (dict): document search request, like {"Name": "John"}
            new_database (str): new destination
            new_collection (str): new destination
        """
        document = await self.findOne(database, collection, query)
        await self.insertOne(new_database, new_collection, document)
        await self.deleteOne(database, collection, query)
        
        
    async def countDocuments(self, database: str, collection: str, query: dict):
        """Count amount of documents in collection
        Args:
            database (str): name of database
            collection (str): name of collection
            query (dict): document search request, like {"status": "active"}

        Returns:
            int : amount
        """
        count = await self.client[database][collection].count_documents(query)
        return count