import os
import time
import requests
from tok import token
URL = 'https://api.vk.com/method/photos.get'
params = {
    'user_id': '87878521',
    'album_id': 'profile',
    'extended': '1',
    'photo_sizes': '1',
    'access_token': token,
    'count': '1000',
    'v': '5.131'
}
res = requests.get(URL, params=params)
for item in res.json()['response']['items']:
    likes_count = item["likes"]["count"]
    if not os.path.exists(f'Photos/{likes_count}.jpg'):
        with open(f'Photos/{likes_count}.jpg', 'wb') as file:
            photo = requests.get(item['sizes'][-1]['url'])
            file.write(photo.content)
    else:
        with open(f'Photos/{likes_count}_{item["date"]}.jpg', 'wb') as file:
            photo = requests.get(item['sizes'][-1]['url'])
            file.write(photo.content)
    time.sleep(0.5)







# pprint(res.json())
# with open('1.json', 'w', encoding='utf-8') as file:
#     json.dump(res.json(), file, indent=4)
