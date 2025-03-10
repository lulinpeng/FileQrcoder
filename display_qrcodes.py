import tkinter as tk 
from PIL import Image, ImageTk
import logging
import os
import utils

# log setting
logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

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

dir_path = './qrcodes/'

qrcodes = os.listdir(dir_path) # get all qrcode images
qrcodes = [dir_path+qrcode for qrcode in qrcodes]

vertical_qrcodes = utils.vertical_concat_img(qrcodes, 2) # concatenate images vertically
horizontal_qrcodes = utils.horizontal_concat_img(vertical_qrcodes, 2) # concatenate images horizontally

width, height = Image.open(horizontal_qrcodes[0]).size

root = tk.Tk()
root.title("Display QR Code")
canvas = tk.Canvas(root, width=width, height=height)
canvas.pack() # put a canvas

time_interval = 500 # ms
qrcode_idx = 0
display_qrcode()

root.mainloop()
