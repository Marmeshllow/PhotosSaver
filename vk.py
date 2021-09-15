import os
from time import sleep
import requests
from tqdm import tqdm


def download_photos(photo_list):
    for item in tqdm(photo_list):
        likes_count = item["likes"]["count"]
        if not os.path.exists(f'Photos/{likes_count}.jpg'):
            with open(f'Photos/{likes_count}.jpg', 'wb') as file:
                photo = requests.get(item['sizes'][-1]['url'])
                file.write(photo.content)
        else:
            with open(f'Photos/{likes_count}_{item["date"]}.jpg', 'wb') as file:
                photo = requests.get(item['sizes'][-1]['url'])
                file.write(photo.content)
        sleep(0.5)


class Vk:
    def __init__(self, token, owner_id):
        self.token = token
        self.owner_id = owner_id
        self.url = 'https://api.vk.com/method/'

    def _get_albums(self):
        params = {
            'owner_id': self.owner_id,
            'photo_sizes': '1',
            'need_system': '1',
            'access_token': self.token,
            'v': '5.131'
        }
        res = requests.get(self.url+'photos.getAlbums', params=params).json()
        try:
            if res['error']['error_code'] == 30:
                return None
        except KeyError:
            return res['response']['items']

    def _get_photos_list(self, album_id):
        params = {
            'owner_id': self.owner_id,
            'album_id': album_id,
            'extended': '1',
            'count': '1000',
            'photo_sizes': '1',
            'access_token': self.token,
            'v': '5.131'
        }
        res = requests.get(self.url+'photos.get', params=params).json()
        download_photos(res['response']['items'])

    def _get_user_photos_list(self):
        params = {
            'user_id': self.owner_id,
            'extended': '1',
            'count': '1000',
            'access_token': self.token,
            'v': '5.131'
        }

        res = requests.get(self.url + 'photos.getUserPhotos', params=params).json()
        download_photos(res['response']['items'])

    def choice_album(self):
        albums = self._get_albums()
        if albums is not None:
            while True:
                print('Введите номер альбома')
                for index, elm in enumerate(albums):
                    print(f'{index}. {elm["title"]} ||| {elm["size"]} фотографии')
                try:
                    choice_alb_num = int(input())
                except ValueError:
                    print('Введите корректное число')
                    continue
                if choice_alb_num in range(0, len(albums)):
                    id_album = albums[choice_alb_num]['id']
                    if id_album != -9000:
                        self._get_photos_list(id_album)
                        print('Success')
                        break
                    else:
                        self._get_user_photos_list()
                        print('Success')
                        break
                else:
                    print('Введите корректное число')
                    continue
        else:
            print('Closed profile')
