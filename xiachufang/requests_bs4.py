from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urlparse

r = requests.get("http://www.xiachufang.com/")
soup = BeautifulSoup(r.text)

img_list = []
for img in soup.select('img'):
    if img.has_attr('data-src'):
        # print(img.attrs['data-src'])
        img_list.append(img.attrs['data-src'])
    else:
        # print(img.attrs['src'])
        img_list.append(img.attrs['src'])

image_dir = os.path.join(os.curdir, "images")

for img in img_list:
    o = urlparse(img)
    filname = o.path[1:].split('@')[0]
    filepath = os.path.join(image_dir, filname)
    if not os.path.isdir(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    url = "%s://%s/%s" % (o.scheme, o.netloc, o.path.split('@')[0])
    print(url)
    resp = requests.get(url)
    with open(filepath, 'wb') as f:
        for chunk in resp.iter_content(4096):
            f.write(chunk)
