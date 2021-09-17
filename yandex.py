import requests
import os
import json
from tqdm import tqdm


def logs(log_list, count):
    data = {
        'response': {
            'count': count,
            'items': log_list
        }
    }
    with open('2.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, file_path: str):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self._get_headers()
        params = {"path": file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path: str):
        href = self._get_upload_link(file_path=file_path).get("href", "")
        response = requests.put(href, data=open(file_path, 'rb'))
        response.raise_for_status()
        if response.status_code != 201:
            print("Upload error")

    def create_folder(self, folder_name: str):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = self._get_headers()
        params = {"path": folder_name}
        requests.put(upload_url, headers=headers, params=params)

    def upload_all(self, folder_name: str):
        log_list = []
        photos_list = os.listdir(folder_name)
        pbar = tqdm(photos_list)
        self.create_folder(folder_name)
        for photo in pbar:
            pbar.set_description('Upload to YD')
            self.upload(f'{folder_name}/{photo}')
            size = os.path.getsize(f'{folder_name}/{photo}')
            log_list.append({'name': photo, 'size': size})
        logs(log_list, len(photos_list))
        print('Success')
