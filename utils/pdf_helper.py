""" pdf helper """
from typing import List
from PIL import Image
from tqdm import tqdm


def merge_images_to_pdf(image_paths: List[str], output: str):
    """ merge images to pdf """
    first_image = None
    rest_images = []
    for i, image_path in tqdm(enumerate(sorted(image_paths, key=lambda x: int(x.split('/')[-1].replace('.png', ''))))):
        img = Image.open(image_path).convert('RGB')
        if i == 0:
            first_image = img
        else:
            rest_images.append(img)

    if first_image:
        first_image.save(output, save_all=True, append_images=rest_images)
