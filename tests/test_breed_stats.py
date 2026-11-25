import time

import pytest

from conftest import fake_api
from src.breed_stats import breeds_statistics, images_for_breeds
from src.dog_client import DogClient

pytestmark = pytest.mark.asyncio


async def test_statistics_counts_breeds_and_sub_breeds():
    routes = {
        "/breeds/list/all": (200, {
            "status": "success",
            "message": {"hound": ["afghan", "basset", "blood"], "pug": [], "bulldog": ["boston", "french"]},
        })
    }

    async with DogClient(transport=fake_api(routes)) as client:
        statistics = await breeds_statistics(client)

    assert statistics == {"total": 3, "with_sub_breeds": 2, "richest_breed": "hound"}


async def test_statistics_without_sub_breeds():
    routes = {"/breeds/list/all": (200, {"status": "success", "message": {"pug": [], "akita": []}})}

    async with DogClient(transport=fake_api(routes)) as client:
        statistics = await breeds_statistics(client)

    assert statistics["with_sub_breeds"] == 0
    assert statistics["richest_breed"] is None


@pytest.mark.network
async def test_statistics_on_real_api(dog_client):
    statistics = await breeds_statistics(dog_client)

    assert statistics["total"] > 50
    assert statistics["richest_breed"] is not None


@pytest.mark.network
async def test_images_for_several_breeds_are_loaded_in_parallel(dog_client):
    breeds = ["pug", "akita", "beagle", "boxer", "husky"]

    started = time.perf_counter()
    images = await images_for_breeds(dog_client, breeds)
    parallel_seconds = time.perf_counter() - started

    assert list(images) == breeds
    assert all(f"/breeds/{breed}/" in images[breed] for breed in breeds)
    print(f"5 запросов параллельно: {parallel_seconds:.2f} с")
