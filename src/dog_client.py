import httpx

BASE_URL = "https://dog.ceo/api"
MAX_IMAGES = 50


class DogApiError(Exception):
    pass


class DogClient:
    def __init__(self, base_url=BASE_URL, transport=None):
        self.http = httpx.AsyncClient(base_url=base_url, transport=transport, timeout=15)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

    async def close(self):
        await self.http.aclose()

    async def _get(self, path):
        response = await self.http.get(path)
        data = response.json()

        if response.status_code != 200 or data.get("status") != "success":
            raise DogApiError(data.get("message", f"Ошибка API, код {response.status_code}"))

        return data["message"]

    async def all_breeds(self):
        return await self._get("/breeds/list/all")

    async def sub_breeds(self, breed):
        return await self._get(f"/breed/{breed.lower()}/list")

    async def breed_image(self, breed):
        return await self._get(f"/breed/{breed.lower()}/images/random")

    async def random_images(self, count):
        if not isinstance(count, int) or count < 1 or count > MAX_IMAGES:
            raise ValueError(f"Количество картинок должно быть от 1 до {MAX_IMAGES}")
        return await self._get(f"/breeds/image/random/{count}")
