import os
import time
import requests
from tqdm import tqdm


def create_folder(folder_name: str):
    while True:
        if os.path.exists(folder_name):
            folder_name = input('Такая папка уже существует\n')
        try:
            os.mkdir(folder_name)
            return folder_name
        except OSError:
            print('Неккорректное имя папки')
            folder_name = input('Введите имя папки для фото\n')
            continue


def download_photos(photo_list: list, album_name: str):
    folder_name = create_folder(album_name)
    pbar = tqdm(photo_list)
    for item in pbar:
        pbar.set_description('Download photos from VK')
        likes_count = item["likes"]["count"]
        if not os.path.exists(f'{folder_name}/{likes_count}.jpg'):
            with open(f'{folder_name}/{likes_count}.jpg', 'wb') as file:
                photo = requests.get(item['sizes'][-1]['url'])
                file.write(photo.content)
        else:
            with open(f'{folder_name}/{likes_count}_{item["date"]}.jpg', 'wb') as file:
                photo = requests.get(item['sizes'][-1]['url'])
                file.write(photo.content)
        time.sleep(0.5)
    return folder_name


class Vk:
    def __init__(self, token: str, owner_id: int):
        self.token = token
        self.owner_id = owner_id
        self.url = 'https://api.vk.com/method/'

    def get_albums(self):
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

    def get_photos_list(self, album_id):
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
        return res

    def get_user_photos_list(self):
        params = {
            'user_id': self.owner_id,
            'extended': '1',
            'count': '1000',
            'photo_sizes': '1',
            'access_token': self.token,
            'v': '5.131'
        }
        res = requests.get(self.url + 'photos.getUserPhotos', params=params).json()
        return res

    def choice_album(self):
        albums = self.get_albums()
        if albums is not None:
            while True:
                print('Введите номер альбома или /q чтобы выйти')
                for index, elm in enumerate(albums):
                    print(f'{index}. {elm["title"]} ||| {elm["size"]} фотографии')
                choice_alb_num = input()
                if choice_alb_num == '/q':
                    break
                try:
                    int(choice_alb_num)
                except ValueError:
                    print('Введите корректное число')
                    continue
                if choice_alb_num in range(0, len(albums)):
                    id_album = albums[choice_alb_num]['id']
                    album_name = albums[choice_alb_num]['title']
                    if id_album != -9000:
                        items = self.get_photos_list(id_album)
                    else:
                        items = self.get_user_photos_list()
                    folder_name = download_photos(items['response']['items'], album_name)
                    print('Success')
                    return folder_name
                else:
                    print('Введите корректное число')
                    continue
        else:
            print('Closed profile or incorrect id')
