import pytest

from src.dog_client import DogApiError

pytestmark = [pytest.mark.asyncio, pytest.mark.network]


async def test_all_breeds_contains_known_breeds(dog_client):
    breeds = await dog_client.all_breeds()

    assert "hound" in breeds
    assert "afghan" in breeds["hound"]


async def test_sub_breeds_of_hound(dog_client):
    sub_breeds = await dog_client.sub_breeds("Hound")

    assert {"afghan", "basset"} <= set(sub_breeds)


async def test_breed_image_is_link_to_breed_photo(dog_client):
    image = await dog_client.breed_image("pug")

    assert image.startswith("https://images.dog.ceo/breeds/pug/")


@pytest.mark.parametrize("count", [1, 5, 50])
async def test_random_images_returns_requested_count(dog_client, count):
    images = await dog_client.random_images(count)

    assert len(images) == count


async def test_unknown_breed_raises_api_error(dog_client):
    with pytest.raises(DogApiError, match="Breed not found"):
        await dog_client.breed_image("unknownbreed")
