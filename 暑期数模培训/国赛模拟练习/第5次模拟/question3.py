import cv2
import imwatermark as wm

im = cv2.imread('original.jpg')
content = '深圳杯数学建模挑战赛'
encoder = wm.WatermarkEncoder()
encoder.set_watermark('bytes', content.encode('utf-8'))
length = encoder.get_length()
im_encode = encoder.encode(im, 'dwtDctSvd')
decoder = wm.WatermarkDecoder(length=length)
png = cv2.imread('compress.png')
watermark_png = decoder.decode(png, 'dwtDctSvd')
resize = cv2.resize(im_encode, (1920, 1080))
cv2.imwrite('resize.jpg', resize)
watermark_resize = decoder.decode(resize, 'dwtDctSvd')
crop = im_encode[0:1080, 0:720]
cv2.imwrite('crop.jpg', crop)
watermark_crop = decoder.decode(crop, 'dwtDctSvd')
rotate = cv2.rotate(im_encode, cv2.ROTATE_90_CLOCKWISE)
cv2.imwrite('rotate.jpg', rotate)
watermark_rotate = decoder.decode(rotate, 'dwtDctSvd')
try:
    watermark_png.decode('utf-8')
except UnicodeDecodeError:
    print('png decode error')
try:
    watermark_resize.decode('utf-8')
except UnicodeDecodeError:
    print('resize decode error')
try:
    watermark_crop.decode('utf-8')
except UnicodeDecodeError:
    print('crop decode error')
try:
    watermark_rotate.decode('utf-8')
except UnicodeDecodeError:
    print('rotate decode error')
