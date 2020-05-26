import aiohttp
import asyncio
import json
import urllib
from datetime import datetime, date, time, timedelta
from tinydb import TinyDB, Query
from utilities.DBHandler import parseCategoryEntries, parseParentCategories
from utilities.ResponseFormatter import getResponseJson
from utilities.SessionTimeManager import sleepTimeout, checkTokenExpiration
from constants.UrlConstants import AUTH_TOKEN_URL, CATEGORY_FETCH_URL, ENTRY_FETCH_URL

async def fetch(session, url, payload, headers):
    async with session.get(url, data = payload, headers = headers) as response:
        return await response.read()

async def getToken():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, AUTH_TOKEN_URL, '', '')
        result = json.loads(html.decode('utf-8'))
        token = result["token"]
        print('Token Obtained -> ' + token)
        return token, datetime.now().timestamp()

# Fetch all parent categories and save them to database
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
            url = CATEGORY_FETCH_URL
            url += str(page)
            headers = {"Authorization": 'Basic ' + str(token)}
            response = await fetch(session, url, '', headers)
            ResponseJson = getResponseJson(response)
            result.append(ResponseJson['categories'])
            if(len(ResponseJson['categories']) < 10):
                await parseParentCategories(result)
                currTimeStamp = await sleepTimeout(60)
                return result, page + 1
            page = page + 1        

# For each category get all pages of entries and save them to database
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
            url = ENTRY_FETCH_URL.format(urllib.parse.urlencode(args))
            headers = {"Authorization": 'Basic ' + str(token)}
            
            response = await fetch(session, url, '', headers)
            reqCounter = reqCounter + 1

            if(reqCounter % 10 == 0):
                currTimeStamp = await sleepTimeout(60)

            responseJson = getResponseJson(response)
            await parseCategoryEntries(category, responseJson['categories'])

            if(len(responseJson['categories']) < 10):
                return reqCounter, tokenTimeStamp

            page = page + 1