import tkinter as tk 
from PIL import Image, ImageTk
import math
import logging

# log setting
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

# concatenate images horizontally
def horizontal_concat_img(img_paths: str, batch_size:int, interval:int = 0):
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
        res_img_path = f'horizontal_concat_qrcode_{str(i).zfill(8)}.png'
        res_img.save(res_img_path)
        res_img_paths.append(res_img_path)
    return res_img_paths

# concatenate images vertically
def vertical_concat_img(img_paths: str, batch_size:int, interval:int = 0):
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
        res_img_path = f'vertical_concat_qrcode_{str(i).zfill(8)}.png'
        res_img.save(res_img_path)
        res_img_paths.append(res_img_path)
    return res_img_paths

def display_qrcode():
    global qrcode_idx, qrcodes, canvas, tk_photo
    canvas.delete("all")  # delete all on the canvas
    logging.debug(f'qrcode_idx = {qrcode_idx}, QR code file = {qrcodes[qrcode_idx]}')
    qrcode_idx += 1
    qrcode_idx %= len(qrcodes)
    img = Image.open(qrcodes[qrcode_idx])
    tk_photo = ImageTk.PhotoImage(img)
    logging.debug(f"width = {tk_photo.width()}, height = {tk_photo.height()}")
    center_x, center_y = width // 2, height // 2
    canvas.create_image(center_x, center_y, image=tk_photo)  # show QR code in the center of canvas
    root.after(time_interval, display_qrcode)  # call 'display_qrcode' after 'time_interval' milliseconds

dir_path = './'
qrcodes = [f"{dir_path}qrcode_{str(i).zfill(8)}.png" for i in range(3)]
qrcodes = ['./qrcode_00000000.png', './qrcode_00000001.png', './qrcode_00000002.png']

qrcodes = vertical_concat_img(qrcodes, 2) # concatenate images horizontally

qrcodes = horizontal_concat_img(qrcodes, 2) # concatenate images horizontally

root = tk.Tk()
root.title("Display QR Code")

width, height = Image.open(qrcodes[0]).size
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack() # put a canvas

time_interval = 500 # ms
qrcode_idx = 0
display_qrcode()

root.mainloop()
