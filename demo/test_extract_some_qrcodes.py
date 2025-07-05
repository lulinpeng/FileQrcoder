import os
import shutil

imgs = [3, 5, 923, 1178, 1902, 2024, 2098, 2170, 2174, 2192, 2296, 2356, 2381, 2544, 2750, 2754, 2756, 2762, 2763, 2776, 2782]

qrcodes_dir = 'qrcodes/'
id = ''
index_len = 5

new_qrcodes_dir = 'new_qrcodes/'
os.makedirs(new_qrcodes_dir, exist_ok=True)

for img in imgs:
    name = f'qrcode_{str(img).zfill(index_len)}.png'
    old_path = os.path.join(f"{qrcodes_dir}{id}", name)
    print(f'path = {old_path}')
    new_path = os.path.join(f"{new_qrcodes_dir}{id}", name)
    shutil.copy(old_path, new_path)