import utils
import os

img_dir = '/Users/Shared/images'
imgs = os.listdir('/Users/Shared/images')
print(imgs)
for img in imgs:
    in_img_path = os.path.join(img_dir, img)
    print(f'in_img_path = {in_img_path}')
    out_dir = 'tmp_flip'
    os.makedirs(out_dir, exist_ok=True)
    out_img_path = f'{out_dir}/{img}'
    print(f'out_img_path = {out_img_path}')
    utils.image_flip(in_img_path, out_img_path, 'vertical')
