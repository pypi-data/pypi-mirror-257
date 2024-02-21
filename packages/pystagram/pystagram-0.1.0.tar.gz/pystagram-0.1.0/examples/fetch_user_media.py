import os
from typing import Any, Dict

from pystagram.graph_api import PystagramGraphApi
from pystagram.graph_api.components.fields.media_fields import MediaFields

graph_api = PystagramGraphApi(
    app_id=1175963656371913,
    app_secret="050c1cda766e5e6cdcba25d44566ce9b",
    access_token="EAAQtiGABvskBOyeOVGpzN6Wt5yeWFdDeuB8X2TbZAvX85ny14wZAYd8gx1HqrhThG5Gr7iNGdkxQPqyb3VOVU1nt6ACw7FV3dq6bNSjMmqh5l2q7XztgKwUjgaktV5mlq0rI2urifw3iI6RLh4ZBDamtC2e2RdpoKoBB7gOWSAMJfrW2dRZA2ynWIyZABJNSl"
)

graph_api.MAX_PAGES = 1


response = graph_api.user.media.get()

media_ids = [media["id"] for media in response.data["data"]]

medias = list()
for media_id in media_ids[:4]:
    response = graph_api.media.get(
        media_id=media_id,
        fields=MediaFields.list(),
    )
    medias.append(response.data)

print(medias)


