import httpx
import pytest_asyncio

from src.dog_client import DogClient


@pytest_asyncio.fixture
async def dog_client():
    async with DogClient() as client:
        yield client


def fake_api(routes):
    def handler(request):
        path = request.url.path.removeprefix("/api")
        status, body = routes.get(path, (404, {"status": "error", "message": "Not found"}))
        return httpx.Response(status, json=body)

    return httpx.MockTransport(handler)
