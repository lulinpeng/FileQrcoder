from PIL import Image
import utils
import random
import math

# generate qrcodes with specified size, i.e., width * height
def gen_qrcodes(n:int, width:int=None, height:int=None):
    qrcodes_png = []
    for i in range(n):
        data = str(i).zfill(7)
        file = f"qrcode_{data}.png"
        qrcodes_png.append(file)
        utils.gen_and_save_qrcode(data, file, QR_CODE_VERSION=8)

    qrcodes = [Image.open(f).convert('RGB') for f in qrcodes_png]
    qr_width, qr_height = qrcodes[0].size
    print(f'gen_qrcodes: QR code width * height = {qr_width} * {qr_height}')
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
    corners = [(0, 0), (width - qr_width, 0), (0, height - qr_height), (width - qr_width, height - qr_height)]
    for i in range(4):
        img.paste(qrcodes[i], corners[i])
    return corners

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
    return (center_x, center_y)

# generate ceils with random colors
def gen_ceils_with_random_color(n:int, color_table:list, width:int, height:int):
    ceils = []
    for i in range(n):
        color_idx = random.randint(0, len(color_table)-1)
        ceils.append(Image.new('RGB', (width, height), color_table[color_idx]))
    return ceils

# generate a colorful code with four corner qrcodes
def gen_color_code_with_corners(rows:int, cols:int, ceil_w:int, ceil_h:int, background_color = (230, 230, 190), outfile:str='color_code_corners.png'):
    print(f'rows = {rows}, cols = {cols}')
    print(f'ceil width = {ceil_w}, ceil_height = {ceil_h}')
    qr_width, qr_height, qrcodes = gen_qrcodes(4)
    width, height = qr_width * 2 + ceil_w * rows, qr_height * 2 + ceil_h * cols
    print(f'width = {width}, height = {height}')

    # new image
    img = Image.new('RGB', (width, height), background_color)

    # put corners
    corners = put_corners(img, qrcodes) 
    print(f'corners = {corners}')

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
    print(f'rows = {rows}, cols = {cols}')
    print(f'ceil width = {ceil_w}, ceil_height = {ceil_h}')
    qr_width, qr_height, qrcodes = gen_qrcodes(4)
    print(f'qr_width = {qr_width}, qr_height = {qr_height}')
    width, height = ceil_w * rows, ceil_h * cols
    print(f'width = {width}, height = {height}')

    # new image
    img = Image.new('RGB', (width, height), background_color)

    # put a qrcode in the center
    center = put_center(img, qrcodes[0]) 

    # put all colorful ceils
    color_table = utils.gen_color_table()
    ceils = gen_ceils_with_random_color(rows * cols, color_table, ceil_w, ceil_h)

    x = 0
    y = 0
    for i in range(rows):
        for j in range(cols):
            x, y = ceil_w * i, ceil_h * j
            if x >= center[0] and x < center[0] + qr_width and y >= center[1] and y < center[1] + qr_height:
                continue
            img.paste(ceils[i * cols + j], (x, y))

    img.save(outfile)
    info_capacity = round((rows * cols - (qr_width * qr_height) / (ceil_h * ceil_w)) * math.log2(len(color_table))/(8*1024), 2)
    print(f'infomation capacity = {info_capacity} KB')
    return outfile

if __name__ == '__main__':
    outfile = gen_color_code_with_corners(rows=130, cols=80, ceil_w=20, ceil_h=20)
    print(f'outfile = {outfile}')

    outfile = gen_color_code_with_center(rows=130, cols=80, ceil_w=20, ceil_h=20)
    print(f'outfile = {outfile}')

