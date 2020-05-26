import aiohttp
import asyncio
from tinydb import TinyDB, Query

# Manages the interface with database for table -> categoryEntryDB
async def parseCategoryEntries(category, entryList):
     db = TinyDB('databases/categoryEntryDB.json')
     categoryEntryDB = db.table('ApiEntries')
     for entry in entryList:
        categoryEntryDB.insert(
            {
                'API' : entry['API'],
                'Link' : entry['Link'],
                'Description' : entry['Description'],
                'Auth' : entry['Auth'],
                'HTTPS' : entry['HTTPS'],
                'Cors' : entry['Cors'],
                'ParentCategory': category
            }
        )

# Manages the interface with database for table -> parentCategoryDB
async def parseParentCategories(categoryListOfList):
     db = TinyDB('databases/parentCategoryDB.json')
     categoryDB = db.table('CategoryEntries')
     for categoryList in categoryListOfList:
        for category in categoryList:
            categoryDB.insert(
                {
                    'Category': category
                }
            )        