from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from database_tools import *


async def main():
    print("Hello world!")


if __name__ == '__main__':
    client = AsyncIOMotorClient('localhost', 27017)
    asyncio.run(main())
    