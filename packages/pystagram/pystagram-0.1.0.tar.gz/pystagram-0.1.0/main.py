from pystagram.graph_api.components.fields.media_fields import MediaFields
from pystagram.graph_api.graph_api import PystagramGraphApi


api = PystagramGraphApi(
    app_id=1175963656371913,
    app_secret="050c1cda766e5e6cdcba25d44566ce9b",
    access_token="EAAQtiGABvskBOyeOVGpzN6Wt5yeWFdDeuB8X2TbZAvX85ny14wZAYd8gx1HqrhThG5Gr7iNGdkxQPqyb3VOVU1nt6ACw7FV3dq6bNSjMmqh5l2q7XztgKwUjgaktV5mlq0rI2urifw3iI6RLh4ZBDamtC2e2RdpoKoBB7gOWSAMJfrW2dRZA2ynWIyZABJNSl"
)


medias = api.user.media.get()

print(len(medias.data))

# f = MediaFields.list()
#
# print(f)

# user_media = api.user.media.get()
#
# media_id="18309597949130858"
#
# print(user_media)
