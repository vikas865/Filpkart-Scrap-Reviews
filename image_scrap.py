import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import  urllib3
import ssl
import os

save_dir = "images/"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

query= "vikas+kumar"
headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
response=requests.get(f"https://www.google.com/search?q={query}&sca_esv=4771c1dce5b9df5f&udm=2&biw=1536&bih=302&ei=vC5CZoTGC7WJ4-EP4Yy7wAg&ved=0ahUKEwiElPzs9YqGAxW1xDgGHWHGDogQ4dUDCBA&uact=5&oq=vikas+kumar&gs_lp=Egxnd3Mtd2l6LXNlcnAiC3Zpa2FzIGt1bWFyMgoQABiABBhDGIoFMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAESNwDUABYAHABeACQAQCYAQCgAQCqAQC4AQPIAQCYAgGgAgmYAwCIBgGSBwExoAcA&sclient=gws-wiz-serp", headers=headers)
#response.content

response_html= bs(response.content, 'html.parser')
all_images= response_html.find_all("img")
del all_images[0]

image_data_lst = []
for i in all_images:
    try:
        image_url = i['data-src']
        image_data = requests.get(image_url).content
        mydict = {'index': image_url, 'image': image_data}
        image_data_lst.append(mydict)
        with open(os.path.join(save_dir, f"{query}_{all_images.index(i)}.jpg"), 'wb') as f:
            f.write(image_data)
    except Exception as e:
        print(e)
