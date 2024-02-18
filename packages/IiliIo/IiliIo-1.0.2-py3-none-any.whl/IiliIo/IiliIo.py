import os
import re
import time
import requests
import argparse
from fake_useragent import UserAgent
from requests_toolbelt.multipart.encoder import MultipartEncoder


class IiliIo:
    def __init__(self):
        self.ua = UserAgent()
        self.user_agent = self.ua.random
        self.auth_token = self._get_auth_token()
        self.contact = "https:/t.me/OneFinalHug"

    def _get_auth_token(self):
        req = requests.get("https://freeimage.host/")
        if req.status_code == 200:
            HUG = re.search(r'[a-zA-Z0-9]{40}', req.text)
            OneFinalHug = HUG[0]
        else:
            OneFinalHug = "3a2d56f454fcea1fa8593d656f862c986950cbb3"
        return OneFinalHug

    def upload_image(self, image_path):
        file_name = os.path.basename(image_path)
        
        headers = {
            'authority': 'imgbb.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'origin': 'https://freeimage.host/',
            'referer': 'https://freeimage.host/',
            'user-agent': self.user_agent,
        }

        try:
            with open(image_path, "rb") as image_file:
                file_content = image_file.read()
        except FileNotFoundError:
            print("Image Not Found")
            return

        data = {
            'source': (file_name, file_content, 'image/jpeg'),
            'type': 'file',
            'action': 'upload',
            'timestamp': str(int(time.time() * 1000)),
            'auth_token': self.auth_token
        }
        m = MultipartEncoder(fields=data)

        headers['Content-Type'] = m.content_type

        response = requests.post('https://freeimage.host/json', headers=headers, data=m)
        if response.status_code == 200:
            re_data = response.json()["image"]
            return re_data
        else:
            return "Oops! Unable to upload the image."

    def upload_url(self, url):
        headers = {
            'Accept': 'application/json',
            'Referer': 'https://freeimage.host/',
            'User-Agent': self.user_agent
        }

        payload = MultipartEncoder(
            fields={
                'source': url,
                'type': 'url',
                'action': 'upload',
                'timestamp': str(int(time.time() * 1000)),
                'auth_token': self.auth_token
            }
        )
        headers['Content-Type'] = payload.content_type

        response = requests.post('https://freeimage.host/json', headers=headers, data=payload)

        if response.status_code == 200:
            re_data = response.json()["image"]
            return re_data
        else:
            return "Oops! Unable to upload the image."

def main():
    parser = argparse.ArgumentParser(description='Upload an image to IiliIo without API key\n it\'s using public API so don\'t use personal or private photos :)')
    parser.add_argument('-i', '--image', help='path to image file to upload')
    parser.add_argument('-u', '--url', help='URL of image to upload')
    args = parser.parse_args()

    uploader = IiliIo()

    if args.image:
        result = uploader.upload_image(args.image)
        print(result)
    elif args.url:
        result = uploader.upload_url(args.url)
        print(result)
    else:
        print("Please provide either an image file or a URL to upload.")

if __name__ == "__main__":
    main()
