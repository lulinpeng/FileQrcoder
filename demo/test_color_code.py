from PIL import Image, ImageDraw
import utils

def create_rect_img(width:int, height:int, color:tuple=(255,255,255)):
    img = Image.new('RGB', (width, height), color)
    return img


def gen_color_table():
    color_table = []
    for i in range(5000):
        color_table.append(((i+10)%251,(i+100) % 251, (i+150) % 251))
    return color_table

if __name__ == '__main__':
    width = 2560
    height = 1600
    ratio = 0.6
    width = round(width * ratio)
    height = round(height * ratio)
    print(f'width = {width}, height = {height}')
    n = 5
    qrcodes_png = []
    for i in range(n):
        data = str(i).zfill(7)
        file = f"qrcode_{data}.png"
        qrcodes_png.append(file)
        utils.gen_and_save_qrcode(data, file)

    qrcodes = [Image.open(f).convert('RGB') for f in qrcodes_png]
    qr_width, qr_height = qrcodes[0].size
    img = Image.new('RGB', (width, height), (230, 230, 190))
    utils.put_subimg(img, qrcodes[0], 0.0, 0.0)
    utils.put_subimg(img, qrcodes[1], 1.0, 0.0)
    utils.put_subimg(img, qrcodes[2], 0.0, 1.0)
    utils.put_subimg(img, qrcodes[3], 1.0, 1.0)

    color_table = gen_color_table()
    i = 0
    w = 20
    h = 20
    x = qr_width
    y = 0
    for i in range(len(color_table)):
        
        if x < width - qr_width - w:
            rect_img = create_rect_img(w, h, color_table[i])
            img.paste(rect_img, (x, y))
            x += w
        else:
            print(i)
            x = qr_width
            y += h
            if y > height:
                break

    img.save('color_code.png')

