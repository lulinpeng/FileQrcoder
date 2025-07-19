from PIL import Image
import math
import logging
import os
import qrcode
import colorsys
import subprocess
import cv2
import sys
import datetime

# log setting
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

# return a string of time stamp
def timestamp_str():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# split range [start, end) into 'num_splits' sub-range equally
def split_range_equally(start:int, end:int, num_splits:int):
    assert(end >= start)
    step = (end - start) // num_splits
    r = [[start + i*step, start + (i+1)*step] for i in range(num_splits)]
    r[-1][-1] = end
    return r

def is_macos():
    return sys.platform == "darwin"
 
# flip an image horizontally or vertically
def image_flip(in_img_path:str, out_img_path:str=None, direction:str='horizontal'):
    assert(direction == 'horizontal' or direction == 'vertical')
    in_img = cv2.imread(in_img_path)
    flag = 0 if direction == 'horizontal' else 1
    out_img = cv2.flip(in_img, flag)
    format = in_img_path.split('.')[-1]
    out_img_path = f'{in_img_path}.{direction}.{format}' if out_img_path is None else out_img_path
    print(f'image_flip: {out_img_path}')
    cv2.imwrite(out_img_path, out_img)
    return 

# extract all frames of a video file into a directory named 'outdir'
def extract_frames(video_file:str, outdir:str):
    outdir = 'video_frames/' if outdir is None else outdir
    os.makedirs(outdir, exist_ok=True)
    # read all frames
    cap = cv2.VideoCapture(video_file)  
    frame_count = math.ceil(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        path = os.path.join(outdir,f"frame_{i:08d}.png")
        cv2.imwrite(path, frame)
        i += 1
        print(f'{i} / {frame_count}-th frame, {path}')
    print(f'{video_file}: fps={cap.get(cv2.CAP_PROP_FPS)}, frame count={frame_count}, width= {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}, height={cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}')
    cap.release()

    print(f'outdir = {outdir}')
    return

# evaluate the total running time of video which is going to be generate from the given images
def evaluate_video_total_running_time(img_dir:str, fps:int):
    images_cnt = len(os.listdir(img_dir))
    trt = round(images_cnt/fps)
    print(f'video trt: {trt} seconds')
    return trt

# convert images into a video
def imgs_to_video(images:list, outfile:str=None, fps:int=15):
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        raise Exception("NOT FOUND FFMPEG")
    images = sorted(images)
    images_txt = 'images.txt'
    with open(images_txt, 'w') as f:
        for image in images:
            f.write(f'file {image}\n')
    img_cnt = len(images)
    outfile = f'out.{timestamp_str()}.mp4' if outfile is None else outfile
    # construct ffmpeg cmd
    cmd = ["ffmpeg", "-r", str(fps),
           "-f", "concat",
           "-safe", "0",
            "-i", images_txt,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-y",  # cover existing file
            outfile]
    print(f'cmd = {cmd}')
    subprocess.run(cmd, check=True)
    return outfile

def heic_to_png(heic_path:str, png_path:str, quality:int=100):
    import heic2png
    heic_img = heic2png.HEIC2PNG(heic_path, quality=90)
    heic_img.save(png_path)
    return 

# generate n highly distinguishable colors
def gen_color_table(n:int = 1024, saturation=0.8, value=0.9):
    colors = []
    for i in range(n):
        hue = i / n  # hue is uniformly distributed between 0 and 1
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        rgb = (int(r * 255), int(g * 255), int(b * 255))
        colors.append(rgb)
    return colors

# generate n uniform distance color
def gen_uniform_color_table():
    t = [i * 32 for i in range(8)]
    colors = []
    for i in range(8):
        for j in range(8):
            for k in range(8):
                colors.append((t[i], t[j], t[k]))
    return colors

# put sub-image 'subimg' at the relative position (x, y) on image 'img'
# 0.0 < x_ratio < 1.0
# 0.0 < y_ratio < 1.0
def put_subimg(img:Image, subimg:Image, x_ratio:float = 0.0, y_ratio:float = 0.0):
    if x_ratio < 0.0 or x_ratio > 1.0 or y_ratio < 0.0 or y_ratio > 1.0:
        error_msg = f'invalid x_ratio = {x_ratio} or y_ratio = {y_ratio}'
        print(error_msg)
        raise BaseException(error_msg)
    
    width, height = img.size
    sub_width, sub_height = subimg.size
    if width < sub_width or height < sub_height:
        error_msg = f'width = {width} < sub_width = {sub_height} or height = {height} < sub_height = {sub_height}'
        print(error_msg)
        raise BaseException(error_msg)
    
    x = math.ceil((width - sub_width) * x_ratio)
    y = math.ceil((height - sub_height) * y_ratio)

    img.paste(subimg, (x,y))
    return


# generate a QR code image for a given string and save it
def gen_and_save_qrcode(data:str, outfile:str='qrcode.png', QR_CODE_CAPATITY_BYTES:int = 7, QR_CODE_VERSION:int = 1, QR_CODE_ERROR_CORRECT = qrcode.constants.ERROR_CORRECT_H):
    if len(data) > QR_CODE_CAPATITY_BYTES:
        error_msg = f'too many bytes: len(data) = {len(data)} > QR_CODE_CAPATITY_BYTES = {QR_CODE_CAPATITY_BYTES}'
        print(error_msg)
        raise BaseException(error_msg)
    qr = qrcode.QRCode(
        version=QR_CODE_VERSION,
        error_correction=QR_CODE_ERROR_CORRECT,
        box_size=4,  # each pixel size which is default by 1
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

def split_image(image_paths:list, rows, cols, outdir:str, margin:float = 0.2):
    logging.debug(f'split_image: outdir = {outdir}')
    os.makedirs(outdir, exist_ok=True)
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
                block_img.save(f'{outdir}split_image_{str(k * cols * rows + i * cols + j).zfill(8)}.png')
                images.append(block_img) # 切割图片并添加到列表中
            
    return images

# concatenate the given images
def concat_img(img_paths: list, row:int, col:int, outdir="./concat/", interval:int = 0):
    logging.debug(f'concat_img: outdir = {outdir}')
    os.makedirs(outdir, exist_ok=True)
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
        res_img_path = f'{outdir}concat_qrcode_{str(k).zfill(8)}.png'
        res_img.save(res_img_path)
        res_img_paths.append(res_img_path)
    return res_img_paths

# concatenate images horizontally
def horizontal_concat_img(img_paths: list, batch_size:int, interval:int = 0, outdir="./horizontal/"):
    logging.debug(f'outdir = {outdir}')
    os.makedirs(outdir, exist_ok=True)
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
        res_img_path = f'{outdir}horizontal_concat_qrcode_{str(i).zfill(8)}.png'
        res_img.save(res_img_path)
        res_img_paths.append(res_img_path)
    return res_img_paths

# concatenate images vertically
def vertical_concat_img(img_paths: list, batch_size:int, interval:int = 0, outdir="./vertical/"):
    os.makedirs(outdir, exist_ok=True)
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
        res_img_path = f'{outdir}vertical_concat_qrcode_{str(i).zfill(8)}.png'
        res_img.save(res_img_path)
        res_img_paths.append(res_img_path)
    return res_img_paths

