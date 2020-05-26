import aiohttp
import asyncio
import json
import urllib
from datetime import datetime, date, time, timedelta
from tinydb import TinyDB, Query
from utilities.DataFetcher import fetch, getToken, getCategories, getEntryForCategory
from utilities.DBHandler import parseCategoryEntries, parseParentCategories
from utilities.ResponseFormatter import getResponseJson
from utilities.SessionTimeManager import sleepTimeout, checkTokenExpiration

if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    categoryListOfList, page = loop.run_until_complete(getCategories())
    token, tokenTimeStamp = loop.run_until_complete(getToken())
    reqCounter = 1
    for categoryList in categoryListOfList:
        for category in categoryList:
            if(loop.run_until_complete(checkTokenExpiration(datetime.now().timestamp(), tokenTimeStamp)) == True):
                token, tokenTimeStamp = loop.run_until_complete(getToken())
                reqCounter = reqCounter + 1
            reqCounter, tokenTimeStamp = loop.run_until_complete(getEntryForCategory(category, page, reqCounter, tokenTimeStamp, token))

    print('Completed Processing')
