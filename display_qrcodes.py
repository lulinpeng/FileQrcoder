import tkinter as tk 
from PIL import Image, ImageTk

def display_qrcode():
    global qrcode_idx, qrcodes, canvas, tk_photo
    canvas.delete("all")  # delete all on the canvas
    print(f'qrcode_idx = {qrcode_idx}, QR code file = {qrcodes[qrcode_idx]}')
    qrcode_idx += 1
    qrcode_idx %= len(qrcodes)
    img = Image.open(qrcodes[qrcode_idx]).resize((WIDTH, HEIGHT))
    tk_photo = ImageTk.PhotoImage(img)
    print(f"{type(tk_photo)}, width = {tk_photo.width()}, height = {tk_photo.height()}")
    x, y = 400, 400
    canvas.create_image(x, y, image=tk_photo)  # show QR code in the center of canvas
    root.after(1000, display_qrcode)  # call 'display_qrcode' after 2 seconds

WIDTH, HEIGHT = 800, 800
dir_path = './'
qrcodes = [f"{dir_path}qrcode_{str(i).zfill(8)}.png" for i in range(3)]
qrcodes = ['./qrcode_00000000.png', './qrcode_00000001.png', './qrcode_00000002.png']
root = tk.Tk()
root.title("Display QR Code")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack() # put a canvas
qrcode_idx = 0
display_qrcode()
root.mainloop()
