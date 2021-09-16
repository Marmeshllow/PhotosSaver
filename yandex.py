import requests
import os


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
        file_name = file_path.split(sep='/')[-1]
        print(file_name)
        href = self._get_upload_link(file_path=file_path).get("href", "")
        response = requests.put(href, data=open(file_path, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

    def create_folder(self, folder_name: str):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = self._get_headers()
        params = {"path": folder_name}
        requests.put(upload_url, headers=headers, params=params)

    def upload_all(self, folder_name: str):
        photos_list = os.listdir(folder_name)
        self.create_folder(folder_name)
        for photo in photos_list:
            self.upload(f'{folder_name}/{photo}')
