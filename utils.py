from PIL import Image
import math
import logging
import os

# log setting
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

# convert a list of images into a GIF picture
def images2gif(img_paths:list, out_gif:str = 'out.gif'):
    images = []
    for i in range(len(img_paths)): 
        img = Image.open(img_paths[i])
        images.append(img)
    images[0].save(out_gif, save_all=True, append_images=images[1:], duration=200, loop=0)
    return

# concatenate images horizontally
def horizontal_concat_img(img_paths: list, batch_size:int, interval:int = 0, out_dir="./horizontal/"):
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

