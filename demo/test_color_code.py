from PIL import Image, ImageDraw
import utils
import random

def put_four_corners(img:Image):
    qrcodes_png = []
    for i in range(4):
        data = str(i).zfill(7)
        file = f"qrcode_{data}.png"
        qrcodes_png.append(file)
        utils.gen_and_save_qrcode(data, file)

    qrcodes = [Image.open(f).convert('RGB') for f in qrcodes_png]
    qr_width, qr_height = qrcodes[0].size
    
    img.paste(qrcodes[0], (0, 0))
    img.paste(qrcodes[1], (width - qr_width, 0))
    img.paste(qrcodes[2], (0, height - qr_height))
    img.paste(qrcodes[3], (width - qr_width, height - qr_height))

    return qr_width, qr_height

if __name__ == '__main__':
    rows, cols = 128, 80
    print(f'rows = {rows}, cols = {cols}')
    ceil_w, ceil_h = 20, 20
    print(f'ceil width = {ceil_w}, ceil_height = {ceil_h}')
    width, height = ceil_w * rows, ceil_h * cols
    print(f'width = {width}, height = {height}')
    background_color = (230, 230, 190)
    img = Image.new('RGB', (width, height), background_color)

    qr_width, qr_height = put_four_corners(img)

    color_table = utils.gen_color_table()

    x = qr_width
    y = qr_height
    for i in range(rows*cols):
        if x < width - qr_width - ceil_w:
            color_idx = random.randint(0, len(color_table)-1)
            rect_img = Image.new('RGB', (ceil_w, ceil_h), color_table[color_idx])
            img.paste(rect_img, (x, y))
            x += ceil_w
        else:
            print(i)
            x = qr_width
            y += ceil_h
            if y > height - qr_height:
                break

    img.save('color_code.png')
