from PIL import Image
import utils
import random

# generate qrcodes with specified size, i.e., width * height
def gen_qrcodes(n:int, width:int=None, height:int=None):
    qrcodes_png = []
    for i in range(n):
        data = str(i).zfill(7)
        file = f"qrcode_{data}.png"
        qrcodes_png.append(file)
        utils.gen_and_save_qrcode(data, file)

    qrcodes = [Image.open(f).convert('RGB') for f in qrcodes_png]
    qr_width, qr_height = qrcodes[0].size
    # resize width
    if width != None:
        for i in range(len(qrcodes)):
            qrcodes[i] = qrcodes[i].resize((width, qr_height))
    qr_width, qr_height = qrcodes[0].size
    # resize heigth
    if height != None:
        for i in range(len(qrcodes)):
            qrcodes[i] = qrcodes[i].resize((qr_width, height))
    qr_width, qr_height = qrcodes[0].size
    return qr_width, qr_height, qrcodes

# put four QRCodes in four corners
def put_corners(img:Image, qrcodes:list):
    width, height = img.size
    qr_width, qr_height = qrcodes[0].size

    img.paste(qrcodes[0], (0, 0))
    img.paste(qrcodes[1], (width - qr_width, 0))
    img.paste(qrcodes[2], (0, height - qr_height))
    img.paste(qrcodes[3], (width - qr_width, height - qr_height))
    return

# put a QRCode in the center
def put_center(img:Image, qrcode:Image):
    width, height = img.size
    qr_width, qr_height = qrcode.size
    center_x, center_y = (width - qr_width) // 2, (height - qr_height) // 2
    if center_x * 2 != width - qr_width or center_y * 2 != height - qr_height:
        error_msg = f'put_center is not even'
        print(error_msg)
        assert(error_msg)
    img.paste(qrcode, (center_x, center_y))
    return

# generate ceils with random colors
def gen_ceils_with_random_color(n:int, color_table:list, width:int, height:int):
    ceils = []
    for i in range(n):
        color_idx = random.randint(0, len(color_table)-1)
        ceils.append(Image.new('RGB', (width, height), color_table[color_idx]))
    return ceils

# generate a colorful code with four corner qrcodes
def gen_color_code_with_corners(rows:int, cols:int, ceil_w:int, ceil_h:int, background_color = (230, 230, 190), outfile:str='color_code_corners.png'):
    rows, cols = 138, 80
    print(f'rows = {rows}, cols = {cols}')
    ceil_w, ceil_h = 20, 20
    print(f'ceil width = {ceil_w}, ceil_height = {ceil_h}')
    qr_width, qr_height, qrcodes = gen_qrcodes(4)
    width, height = qr_width * 2 + ceil_w * rows, qr_height * 2 + ceil_h * cols
    print(f'width = {width}, height = {height}')

    # new image
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

    img.save(outfile)
    return outfile

# generate a colorful code with a center qrcode
def gen_color_code_with_center(rows:int, cols:int, ceil_w:int, ceil_h:int, background_color:tuple = (230, 230, 190), outfile:str='color_code_center.png'):
    rows, cols = 138, 80
    print(f'rows = {rows}, cols = {cols}')
    ceil_w, ceil_h = 20, 20
    print(f'ceil width = {ceil_w}, ceil_height = {ceil_h}')
    qr_width, qr_height, qrcodes = gen_qrcodes(4, 168, 168)
    print(f'qr_width = {qr_width}, qr_height = {qr_height}')
    width, height = qr_width * 2 + ceil_w * rows, qr_height * 2 + ceil_h * cols
    print(f'width = {width}, height = {height}')

    # new image
    img = Image.new('RGB', (width, height), background_color)

    # put corners
    put_center(img, qrcodes[0]) 

    # # put all colorful ceils
    # color_table = utils.gen_color_table()
    # ceils = gen_ceils_with_random_color(rows * cols, color_table, ceil_w, ceil_h)

    # x = qr_width
    # y = qr_height
    # for i in range(rows):
    #     for j in range(cols):
    #         x, y = qr_width + ceil_w * i, qr_height + ceil_h * j,
    #         img.paste(ceils[i * cols + j], (x, y))

    img.save(outfile)
    return outfile

if __name__ == '__main__':
    outfile = gen_color_code_with_corners(rows=130, cols=80, ceil_w=20, ceil_h=20)
    print(f'outfile = {outfile}')

    outfile = gen_color_code_with_center(rows=130, cols=80, ceil_w=20, ceil_h=20)
    print(f'outfile = {outfile}')

