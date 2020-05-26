import asyncio
from datetime import datetime, date, time, timedelta

async def sleepTimeout(sleep):
    await asyncio.sleep(sleep)
    return datetime.now().timestamp()


async def checkTokenExpiration(currTimeStamp ,tokenTimeStamp):
    if(currTimeStamp - tokenTimeStamp > 5):
        return True
    return False      