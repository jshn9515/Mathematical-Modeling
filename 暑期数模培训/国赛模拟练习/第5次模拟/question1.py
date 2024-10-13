import cv2
import imwatermark as wm

im = cv2.imread('original.jpg')
content = '深圳杯数学建模挑战赛'
encoder = wm.WatermarkEncoder()
encoder.set_watermark('bytes', content.encode('utf-8'))
im_encode = encoder.encode(im, 'dwtDctSvd')
length = encoder.get_length()
cv2.imwrite('encode1.jpg', im_encode)
decoder = wm.WatermarkDecoder(length=length)
watermark = decoder.decode(im_encode, 'dwtDctSvd')
print(watermark.decode('utf-8'))
