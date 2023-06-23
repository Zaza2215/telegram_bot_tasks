import aiohttp
import asyncio

from dotenv import load_dotenv


load_dotenv()

auth = {
    "username": "user_1",
    "password": "Password_1"
}


async def send_request(url, data, method: str):
    data.update(auth)

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
    data.update(auth)

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