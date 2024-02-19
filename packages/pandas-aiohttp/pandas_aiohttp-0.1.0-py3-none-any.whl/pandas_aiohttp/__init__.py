import pandas as pd
import asyncio
from aiohttp import ClientSession, TCPConnector

@pd.api.extensions.register_series_accessor("aiohttp")
class AiohttpAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    async def _fetch_text(self, url: str, session):
        async with session.get(url) as response:
            return await response.text()
        
    async def _fetch_json(self, url: str, session):
        async with session.get(url) as response:
            return await response.json()

    async def get_text(self, limit:int=100,ssl: bool=True):
        async with ClientSession(connector=TCPConnector(limit=limit, ssl=ssl)) as session:
            work = [self._fetch_text(url, session) for url in self._obj]
            responses = await asyncio.gather(*work)
        return pd.Series(responses)
    
    async def get_json(self, limit:int=100,ssl: bool=True):
        async with ClientSession(connector=TCPConnector(limit=limit, ssl=ssl)) as session:
            work = [self._fetch_json(url, session) for url in self._obj]
            responses = await asyncio.gather(*work)
        return pd.Series(responses)