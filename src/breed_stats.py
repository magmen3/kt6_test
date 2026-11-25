import asyncio


async def breeds_statistics(client):
    breeds = await client.all_breeds()

    with_sub_breeds = {breed: subs for breed, subs in breeds.items() if subs}

    if with_sub_breeds:
        richest_breed = max(with_sub_breeds, key=lambda breed: len(with_sub_breeds[breed]))
    else:
        richest_breed = None

    return {
        "total": len(breeds),
        "with_sub_breeds": len(with_sub_breeds),
        "richest_breed": richest_breed,
    }


async def images_for_breeds(client, breeds):
    images = await asyncio.gather(*(client.breed_image(breed) for breed in breeds))
    return dict(zip(breeds, images))
