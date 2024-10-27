from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from database_tools import *
from classes.table import Table
from classes.order import Order
from classes.item import Item


async def main():
    print("Hello World!")
    

if __name__ == '__main__':
    client = AsyncIOMotorClient('localhost', 27017)
    asyncio.run(main())
    