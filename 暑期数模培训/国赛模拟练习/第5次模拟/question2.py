import cv2
import requests
import imwatermark as wm
from bs4 import BeautifulSoup

url = 'https://www.gov.cn/guoqing/2021-10/29/content_5647633.htm'
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')
content = soup.find('div', {'class': 'pages_content'})
content = content.text.strip()
with open('encode.txt', 'w', encoding='utf-8') as f:
    f.write(content)
im = cv2.imread('original.jpg')
encoder = wm.WatermarkEncoder()
encoder.set_watermark('bytes', content.encode('utf-8'))
im_encode = encoder.encode(im, 'dwtDctSvd')
length = encoder.get_length()
cv2.imwrite('encode2.jpg', im_encode)
decoder = wm.WatermarkDecoder(length=length)
watermark = decoder.decode(im_encode, 'dwtDctSvd')
text = watermark.decode('utf-8', errors='ignore')
with open('decode.txt', 'w', encoding='utf-8') as f:
    f.write(text)
