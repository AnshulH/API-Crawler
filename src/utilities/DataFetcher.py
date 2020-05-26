import aiohttp
import asyncio
import json
import urllib
from datetime import datetime, date, time, timedelta
from tinydb import TinyDB, Query

async def fetch(session, url, payload, headers):
    async with session.get(url, data = payload, headers = headers) as response:
        return await response.read()

async def sleepTimeout(sleep):
    await asyncio.sleep(sleep)
    return datetime.now().timestamp()
    
async def getToken():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'https://public-apis-api.herokuapp.com/api/v1/auth/token', '', '')
        result = json.loads(html.decode('utf-8'))
        token = result["token"]
        print('Token Obtained -> ' + token)
        return token, datetime.now().timestamp()

async def getCategories():
    async with aiohttp.ClientSession() as session:
        page = 1 # Beginning with first page
        result = []
        token, tokenTimeStamp = await getToken()
        currTimeStamp = datetime.now().timestamp()
        while True:
            if(page % 10 == 1 and page != 1):
                currTimeStamp = await sleepTimeout(60)
            if(await checkTokenExpiration(currTimeStamp, tokenTimeStamp) == True):
                token, tokenTimeStamp = await getToken()
            url = 'https://public-apis-api.herokuapp.com/api/v1/apis/categories?page='
            url += str(page)
            headers = {"Authorization": 'Basic ' + str(token)}
            response = await fetch(session, url, '', headers)
            ResponseJson = getResponseJson(response)
            result.append(ResponseJson['categories'])
            # print(result)
            if(len(ResponseJson['categories']) < 10):
                currTimeStamp = await sleepTimeout(60)
                return result, page + 1
            page = page + 1     

def getResponseJson(response):
    return json.loads(response.decode('utf-8'))

def parseCategoryEntries(category, entryList, db):
    print(entryList)
    print()    

async def checkTokenExpiration(currTimeStamp ,tokenTimeStamp):
    if(currTimeStamp - tokenTimeStamp > 5):
        return True
    return False     

async def getEntryForCategory(category, currpage, reqCounter, tokenTimeStamp, token):
    async with aiohttp.ClientSession() as session:
        page = 1 # Beginning with first page
        reqCounter = reqCounter
        currTimeStamp = datetime.now().timestamp()
        if(reqCounter % 10 == 0):
                currTimeStamp = await sleepTimeout(60)
        while True:
            if(await checkTokenExpiration(currTimeStamp, tokenTimeStamp) == True):
                token, tokenTimeStamp = await getToken()
                reqCounter = reqCounter + 1    

            if(reqCounter % 10 == 0):
                currTimeStamp = await sleepTimeout(60)

            args = {"page" : page, "category" : category}
            url = "https://public-apis-api.herokuapp.com/api/v1/apis/entry?{}".format(urllib.parse.urlencode(args))
            headers = {"Authorization": 'Basic ' + str(token)}
            
            response = await fetch(session, url, '', headers)
            reqCounter = reqCounter + 1

            if(reqCounter % 10 == 0):
                currTimeStamp = await sleepTimeout(60)

            responseJson = getResponseJson(response)
            parseCategoryEntries(category, responseJson['categories'], '')

            if(len(responseJson['categories']) < 10):
                return reqCounter, tokenTimeStamp

            page = page + 1
