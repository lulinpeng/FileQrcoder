import tkinter as tk
from PIL import Image, ImageTk
import os

class ImagePlayer:
    def __init__(self, root, image_paths):
        self.root = root
        self.image_paths = image_paths
        self.images = []  # 存储所有图片对象
        
        # 预加载图片并检查路径
        self.load_images()
        
        # 初始化界面
        self.current_idx = 0
        self.label = tk.Label(root)
        self.label.pack()
        self.show_image()

    def load_images(self):
        """加载并验证所有图片"""
        for path in self.image_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"路径错误：{path}")  # 显式报错‌:ml-citation{ref="5,6" data="citationList"}
            img = Image.open(path)
            self.images.append(ImageTk.PhotoImage(img))  # 强制保留引用‌:ml-citation{ref="1,4" data="citationList"}

    def show_image(self):
        """显示当前图片并触发自动切换"""
        if self.images:
            self.label.config(image=self.images[self.current_idx])
            self.current_idx = (self.current_idx + 1) % len(self.images)
        self.root.after(2000, self.show_image)  # 每2秒切换‌:ml-citation{ref="4" data="citationList"}

if __name__ == "__main__":
    root = tk.Tk()
    image_paths = ["/绝对路径/test1.png", "/绝对路径/test2.jpg"]  # 替换为实际路径
    dir_path = '/Users/lulinpeng/Codes/FileQrcoder/qrcodes/'
    qrcodes = os.listdir(dir_path) # get all qrcode images
    image_paths = [dir_path + qrcode for qrcode in qrcodes]
    print(image_paths)
    try:
        ImagePlayer(root, image_paths)
        root.mainloop()
    except Exception as e:
        print("运行错误：", e)

# import tkinter as tk
# from PIL import Image, ImageTk
# import os

# class ImagePlayer:
#     def __init__(self, root, image_paths, interval=2000):
#         self.root = root
#         self.image_paths = image_paths  # 图片文件路径列表
#         self.interval = interval        # 自动播放间隔（毫秒）
#         self.current_idx = 0            # 当前播放索引
        
#         # 预加载所有图片（假设图片尺寸相同）
#         self.images = []
#         for path in image_paths:
#             img = Image.open(path)
#             print(path)
#             self.images.append(ImageTk.PhotoImage(img))  # 必须存储引用 ‌:ml-citation{ref="1,2" data="citationList"}
        
#         # 初始化界面组件
#         self.label = tk.Label(root)
#         self.label.pack()
#         self.show_image()
        
#         # 添加控制按钮（可选）
#         self.add_controls()

#     def show_image(self):
#         """显示当前图片并触发自动切换"""
#         self.label.config(image=self.images[self.current_idx])
#         self.current_idx = (self.current_idx + 1) % len(self.images)
#         self.root.after(self.interval, self.show_image)  # 定时循环 ‌:ml-citation{ref="1,2" data="citationList"}

#     def add_controls(self):
#         """添加手动控制按钮"""
#         btn_frame = tk.Frame(self.root)
#         btn_frame.pack(pady=10)
        
#         # 上一张按钮
#         tk.Button(btn_frame, text="上一张", command=lambda: self.update_image(-1)).pack(side=tk.LEFT)
#         # 下一张按钮
#         tk.Button(btn_frame, text="下一张", command=lambda: self.update_image(1)).pack(side=tk.LEFT)

#     def update_image(self, step):
#         """手动切换图片（step=1为下一张，step=-1为上一张）"""
#         self.current_idx = (self.current_idx + step) % len(self.images)
#         self.label.config(image=self.images[self.current_idx])  # 即时更新显示 ‌:ml-citation{ref="2,3" data="citationList"}

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("图片播放器")
    
#     dir_path = './qrcodes/'
#     qrcodes = os.listdir(dir_path) # get all qrcode images
#     image_paths = [dir_path + qrcode for qrcode in qrcodes]

#     # 替换为实际图片路径列表（示例）
#     # image_paths = ["image1.png", "image2.png", "image3.png"]
    
#     # 初始化播放器（自动播放间隔设为3秒）
#     player = ImagePlayer(root, image_paths, interval=3000)
#     root.mainloop()


# # import tkinter as tk 
# # from PIL import Image, ImageTk
# # import logging
# # import os
# # import utils

# # # log setting
# # logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
# #                     datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

# # def display_qrcode():
# #     global qrcode_idx, qrcodes, canvas, tk_photo
# #     canvas.delete("all")  # delete all on the canvas
# #     logging.debug(f'qrcode_idx = {qrcode_idx}, QR code file = {qrcodes[qrcode_idx]}')
# #     qrcode_idx += 1
# #     qrcode_idx %= len(qrcodes)
# #     img = Image.open(qrcodes[qrcode_idx])
# #     tk_photo = ImageTk.PhotoImage(img)
# #     logging.debug(f"width = {tk_photo.width()}, height = {tk_photo.height()}")
# #     center_x, center_y = width // 2, height // 2
# #     canvas.create_image(center_x, center_y, image=tk_photo)  # show QR code in the center of canvas
# #     root.after(time_interval, display_qrcode)  # call 'display_qrcode' after 'time_interval' milliseconds

# # dir_path = './qrcodes/'

# # qrcodes = os.listdir(dir_path) # get all qrcode images
# # qrcodes = [dir_path+qrcode for qrcode in qrcodes]

# # vertical_qrcodes = utils.vertical_concat_img(qrcodes, 2) # concatenate images vertically
# # horizontal_qrcodes = utils.horizontal_concat_img(vertical_qrcodes, 2) # concatenate images horizontally

# # width, height = Image.open(horizontal_qrcodes[0]).size

# # root = tk.Tk()
# # root.title("Display QR Code")
# # canvas = tk.Canvas(root, width=width, height=height)
# # canvas.pack() # put a canvas

# # time_interval = 500 # ms
# # qrcode_idx = 0
# # display_qrcode()

# # root.mainloop()
