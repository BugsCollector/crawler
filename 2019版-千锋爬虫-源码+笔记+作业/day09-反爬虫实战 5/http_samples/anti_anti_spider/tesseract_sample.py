import os
import sys
import pytesseract
from PIL import Image


def color2gray(path):
    print(path, end=' ')
    img = Image.open(path)
    img = img.convert('L')
    # img.show()
    # 对图片进行黑白转换
    # 图片都是数据组成
    # 对于黑白图片，像素值是0：黑，255：白
    data = img.load()
    w, h = img.size
    for i in range(w):
        for j in range(h):
            if data[i, j] > 135:
                data[i, j] = 255
            else:
                data[i, j] = 0
    # img.show()
    img_name = os.path.basename(path)
    name, subfix = img_name.split('.')
    gray_img_name = '%s.gray.%s' % (name, subfix)
    gray_img = os.path.join(os.path.dirname(path), gray_img_name)
    # print(gray_img)
    img.save(gray_img)
    return gray_img


if __name__ == '__main__':
    if len(sys.argv) > 1:
        imgs = sys.argv[1:]
        for img in imgs:
            gray_img = color2gray(img)
            result = pytesseract.image_to_string(Image.open(gray_img))
            print('result: %s' % result)
