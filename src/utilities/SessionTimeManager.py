import asyncio
from datetime import datetime, date, time, timedelta

# Rate Limit currently is 60 seconds
# Makes the system sleep for specified duration
async def sleepTimeout(sleep):
    await asyncio.sleep(sleep)
    return datetime.now().timestamp()

# Compares two time stamps 
# Checks whether token has expired or not
async def checkTokenExpiration(currTimeStamp ,tokenTimeStamp):
    if(currTimeStamp - tokenTimeStamp > 5):
        return True
    return False      
