import pytest

from conftest import fake_api
from src.dog_client import DogApiError, DogClient

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("count", [0, 51, -5, "10"])
async def test_invalid_count_is_rejected_without_request(count):
    async with DogClient(transport=fake_api({})) as client:
        with pytest.raises(ValueError):
            await client.random_images(count)


async def test_error_status_in_body_raises_api_error():
    routes = {"/breeds/list/all": (200, {"status": "error", "message": "Maintenance"})}

    async with DogClient(transport=fake_api(routes)) as client:
        with pytest.raises(DogApiError, match="Maintenance"):
            await client.all_breeds()


async def test_server_error_without_message_raises_api_error():
    routes = {"/breeds/list/all": (500, {})}

    async with DogClient(transport=fake_api(routes)) as client:
        with pytest.raises(DogApiError, match="код 500"):
            await client.all_breeds()


async def test_breed_name_is_lowercased_in_request():
    routes = {"/breed/pug/list": (200, {"status": "success", "message": []})}

    async with DogClient(transport=fake_api(routes)) as client:
        assert await client.sub_breeds("PUG") == []


async def test_close_closes_http_client():
    client = DogClient(transport=fake_api({}))

    await client.close()

    assert client.http.is_closed
