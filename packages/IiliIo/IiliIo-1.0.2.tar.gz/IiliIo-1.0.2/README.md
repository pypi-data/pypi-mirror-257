# IiliIo public Uploader 
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/onefinalhug) 

![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)

### Upload Images without API key
- Unlimited uploads
- No API limit
- Support Url & Local upload 

⚠️ **Warning**: Do not upload private or personal pictures because this library uses the Imgbb public API

## Install
```
pip install IiliIo
```
## Example use

#### Local upload

```
from IiliIo import IiliIo

upload = IiliIo()
up = upload.upload_image("Drive/lol/ofh.jpg")#full image path
print(up)
```
```
>>> IiliIo -i Drive/lol/ofh.jpg
```
#### Url upload
```
from IiliIo import IiliIo

upload = IiliIo()
up = upload.upload_url("https://i.pinimg.com/originals/fe/ea/71/feea71eaa793b00d9e927985a9d4b199.jpg")
print(up)
```
```
IiliIo -u https://i.pinimg.com/originals/fe/ea/71/feea71eaa793b00d9e927985a9d4b199.jpg
```
