from PIL import Image
import math
import logging
import os
import qrcode

# log setting
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

# generate a QR code image for a given string and save it
def gen_and_save_qrcode(data:str, outfile:str='qrcode.png', QR_CODE_CAPATITY_BYTES:int = 7, QR_CODE_VERSION:int = 1, QR_CODE_ERROR_CORRECT = qrcode.constants.ERROR_CORRECT_H):
    if len(data) > QR_CODE_CAPATITY_BYTES:
        error_msg = f'too many bytes: len(data) = {len(data)} > QR_CODE_CAPATITY_BYTES = {QR_CODE_CAPATITY_BYTES}'
        print(error_msg)
        raise error_msg
    qr = qrcode.QRCode(
        version=QR_CODE_VERSION,
        error_correction=QR_CODE_ERROR_CORRECT,
        box_size=3,  # each pixel size which is default by 1
        border=0,  # frame width which is default by 4
    )
    qr.add_data(data) # add data
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white") # create QR code image
    img.save(outfile)
    return

# convert a list of images into a GIF picture
def images2gif(img_paths:list, out_gif:str = 'out.gif'):
    images = []
    for i in range(len(img_paths)): 
        logging.debug(f'images2gif: img_path = {img_paths[i]}')
        img = Image.open(img_paths[i])
        images.append(img)
    images[0].save(out_gif, save_all=True, append_images=images[1:], duration=200, loop=0)
    return

def extend_margin(x0:int, y0:int, x1:int, y1:int, margin_w:int, margin_h:int, w:int, h:int):
    logging.debug(f'extend_margin start: x0 = {x0}, y0 = {y0}, x1 = {x1}, y1 = {y1}, margin_w = {margin_w}, margin_y = {margin_w}, w = {w}, h = {h}')
    if y0 - margin_w >= 0:
        y0 -= margin_w
    if y1 + margin_w <= w:
        y1 += margin_w

    if x0 - margin_h >= 0:
        x0 -= margin_h
    if x1 + margin_h <= h:
        x1 += margin_h
    logging.debug(f'extend_margin end: x0 = {x0}, y0 = {y0}, x1 = {x1}, y1 = {y1}, margin_w = {margin_w}, margin_y = {margin_w}, w = {w}, h = {h}')
    return x0, y0, x1, y1

def split_image(image_paths:list, rows, cols, out_dir:str, margin:float = 0.2):
    logging.debug(f'split_image: out_dir = {out_dir}')
    os.makedirs(out_dir, exist_ok=True)
    img = Image.open(image_paths[0])
    w, h = img.size # 获取图片的宽度和高度
    logging.debug(f'split_image: w = {w}, h = {h}')
    block_w = w // cols
    block_h = h // rows
    images = []

    add_w = round(block_w * margin)
    add_h = round(block_h * margin)
    for k in range(len(image_paths)):
        for i in range(rows):
            for j in range(cols):
                x0, x1 = j * block_w, (j + 1) * block_w
                y0, y1 = i * block_h, (i + 1) * block_h

                x0, y0, x1, y1 = extend_margin(x0, y0, x1, y1, add_w, add_h, w, h)
                
                block_img = img.crop((x0, y0, x1, y1))
                block_img.save(f'{out_dir}split_image_{str(k * cols * rows + i * cols + j).zfill(8)}.png')
                images.append(block_img) # 切割图片并添加到列表中
            
    return images

# concatenate the given images
def concat_img(img_paths: list, row:int, col:int, out_dir="./concat/", interval:int = 0):
    logging.debug(f'concat_img: out_dir = {out_dir}')
    os.makedirs(out_dir, exist_ok=True)
    first_img = Image.open(img_paths[0])
    width, height = first_img.size
    logging.debug(f'width = {width}, height = {height}')
    batch = row * col
    n = math.ceil(len(img_paths) / batch)
    res_img_paths = []
    for k in range(n): # for each batch
        res_img = Image.new('1', ((width+interval) * col, (height + interval) * row))
        for i in range(row):
            for j in range(col):
                idx = k * batch + i * col + j
                if idx < len(img_paths):
                    logging.debug(f'img_paths[{idx}] = {img_paths[idx]}')
                    img = Image.open(img_paths[idx]).resize((width, height))
                    res_img.paste(img, box=((width+interval)*j , (height+interval)*i))
        res_img_path = f'{out_dir}concat_qrcode_{str(k).zfill(8)}.png'
        res_img.save(res_img_path)
        res_img_paths.append(res_img_path)
    return res_img_paths

# concatenate images horizontally
def horizontal_concat_img(img_paths: list, batch_size:int, interval:int = 0, out_dir="./horizontal/"):
    logging.debug(f'out_dir = {out_dir}')
    os.makedirs(out_dir, exist_ok=True)
    first_img = Image.open(img_paths[0])
    width, height = first_img.size
    logging.debug(f'width = {width}, height = {height}')
    n = math.ceil(len(img_paths) / batch_size)
    res_img_paths = []
    for i in range(n):
        res_img = Image.new('1', ((width+interval) * batch_size, height))
        for j in range(batch_size):
            idx = i * batch_size + j
            if idx< len(img_paths):
                logging.debug(f'img_paths[idx] = {img_paths[idx]}')
                img = Image.open(img_paths[idx]).resize((width, height))
                res_img.paste(img, box=((width+interval)*j , 0))
        res_img_path = f'{out_dir}horizontal_concat_qrcode_{str(i).zfill(8)}.png'
        res_img.save(res_img_path)
        res_img_paths.append(res_img_path)
    return res_img_paths

# concatenate images vertically
def vertical_concat_img(img_paths: list, batch_size:int, interval:int = 0, out_dir="./vertical/"):
    os.makedirs(out_dir, exist_ok=True)
    first_img = Image.open(img_paths[0])
    width, height = first_img.size
    logging.debug(f'width = {width}, height = {height}')
    n = math.ceil(len(img_paths) / batch_size)
    res_img_paths = []
    for i in range(n):
        res_img = Image.new('1', (width, (height + interval) *batch_size))
        for j in range(batch_size):
            idx = i * batch_size + j
            if idx< len(img_paths):
                logging.debug(f'img_paths[idx] = {img_paths[idx]}')
                img = Image.open(img_paths[idx]).resize((width, height))
                res_img.paste(img, box=(0 , (height+interval)*j))
        res_img_path = f'{out_dir}vertical_concat_qrcode_{str(i).zfill(8)}.png'
        res_img.save(res_img_path)
        res_img_paths.append(res_img_path)
    return res_img_paths

