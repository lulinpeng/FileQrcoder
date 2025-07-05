import utils
import os

img_dir = '/Users/Shared/images'
imgs = os.listdir('/Users/Shared/images')
print(imgs)
for img in imgs:
    in_img_path = os.path.join(img_dir, img)
    print(f'in_img_path = {in_img_path}')
    outdir = 'tmp_flip'
    os.makedirs(outdir, exist_ok=True)
    out_img_path = f'{outdir}/{img}'
    print(f'out_img_path = {out_img_path}')
    utils.image_flip(in_img_path, out_img_path, 'vertical')
