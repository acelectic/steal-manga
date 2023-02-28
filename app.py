""" Main Module """
import os
from man_mirror import ManMirror
from utils.pdf_helper import merge_images_to_pdf


if __name__ == "__main__":
    man_mirror = ManMirror()
    # man_mirror.download_cartoons(10)
    target_image_dir = 'files/cartoons/man-mirror/10/chapter-1'
    image_paths = []
    for file in os.listdir(target_image_dir):
        if file.endswith('.png'):
            image_paths.append(f'{target_image_dir}/{file}')
    merge_images_to_pdf(image_paths, f'{target_image_dir}/merge.pdf')
