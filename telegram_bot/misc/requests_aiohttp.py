import aiohttp
import asyncio


async def send_request(url, data, method: str):
    async with aiohttp.ClientSession() as session:

        if method == "GET":
            async with session.get(url, data=data) as response:
                return response
        elif method == "POST":
            async with session.post(url, data=data) as response:
                return response
        elif method == "PUT":
            async with session.put(url, data=data) as response:
                return response
        elif method == "DELETE":
            async with session.delete(url, data=data) as response:
                return response
        else:
            return "This method is not implemented"


async def send_request_json(url, data, method: str):
    async with aiohttp.ClientSession() as session:

        if method == "GET":
            async with session.get(url, data=data) as response:
                return await response.json()
        elif method == "POST":
            async with session.post(url, data=data) as response:
                return await response.json()
        elif method == "PUT":
            async with session.put(url, data=data) as response:
                return await response.json()
        elif method == "DELETE":
            async with session.delete(url, data=data) as response:
                return await response.json()
        else:
            return "This method is not implemented"