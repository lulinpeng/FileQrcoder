from PIL import Image
import utils
import random

def gen_qrcodes(n:int):
    qrcodes_png = []
    for i in range(n):
        data = str(i).zfill(7)
        file = f"qrcode_{data}.png"
        qrcodes_png.append(file)
        utils.gen_and_save_qrcode(data, file)

    qrcodes = [Image.open(f).convert('RGB') for f in qrcodes_png]
    qr_width, qr_height = qrcodes[0].size
    return qr_width, qr_height, qrcodes

def put_corners(img:Image, qrcodes):
    width, height = img.size
    qr_width, qr_height = qrcodes[0].size

    img.paste(qrcodes[0], (0, 0))
    img.paste(qrcodes[1], (width - qr_width, 0))
    img.paste(qrcodes[2], (0, height - qr_height))
    img.paste(qrcodes[3], (width - qr_width, height - qr_height))
    return

def gen_ceils_with_random_color(n:int, color_table:list, width:int, height:int):
    ceils = []
    for i in range(n):
        color_idx = random.randint(0, len(color_table)-1)
        ceils.append(Image.new('RGB', (width, height), color_table[color_idx]))
    return ceils


def put_ceils(img:Image):
    x = qr_width
    y = qr_height
    for i in range(rows):
        for j in range(cols):
            color_idx = random.randint(0, len(color_table)-1)
            print(i,j, color_idx)
            rect_img = Image.new('RGB', (ceil_w, ceil_h), color_table[color_idx])
            x, y = qr_width + ceil_w * i, qr_height + ceil_h * j,
            img.paste(rect_img, (x, y))

if __name__ == '__main__':
    rows, cols = 128, 80
    print(f'rows = {rows}, cols = {cols}')
    ceil_w, ceil_h = 20, 20
    print(f'ceil width = {ceil_w}, ceil_height = {ceil_h}')
    qr_width, qr_height, qrcodes = gen_qrcodes(4)
    width, height = qr_width * 2 + ceil_w * rows, qr_height * 2 + ceil_h * cols
    print(f'width = {width}, height = {height}')

    # new image
    background_color = (230, 230, 190)
    img = Image.new('RGB', (width, height), background_color)

    # put corners
    put_corners(img, qrcodes) 

    # put all colorful ceils
    color_table = utils.gen_color_table()
    ceils = gen_ceils_with_random_color(rows * cols, color_table, ceil_w, ceil_h)

    x = qr_width
    y = qr_height
    for i in range(rows):
        for j in range(cols):
            x, y = qr_width + ceil_w * i, qr_height + ceil_h * j,
            img.paste(ceils[i * cols + j], (x, y))

    img.save('color_code.png')
