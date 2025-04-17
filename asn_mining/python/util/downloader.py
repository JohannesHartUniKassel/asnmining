import os.path as path
import requests


def download(url, dest):
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest, 'wb') as f:
            f.write(response.content)
    return path.abspath(dest)