import os

from pystagram.graph_api import PystagramGraphApi, ImageContainer


graph_api = PystagramGraphApi(
    app_id=int(os.getenv("APP_ID")),
    app_secret=os.getenv("APP_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
)

container = ImageContainer(
    image_url="https://www.example.com/image.jpg",
    caption="your caption #hashtag",
)

response = graph_api.user.media.create(container)
container_id = response.data["id"]


graph_api.user.media_publish.create(container_id=container_id)
