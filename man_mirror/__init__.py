"""Module providingFunction printing python version."""
import os
import random
from time import process_time, sleep
import requests
import imageio.v3 as iio
from man_mirror.image_json_shuffle import ImageJsonShuffle
from utils.constants import CARTOON_DIR
import numpy as np
from utils.file_helper import mkdir
from PIL import Image

HOST = 'https://www.manmirror.net'


class RequestError(Exception):
    """ RequestError """

    def __init__(self, *args: object):
        self.args = args


class ManMirror:
    """ class """

    def download_cartoons(self, post_id: int) -> None:
        """ download man mirror by post id """
        main_dir = f'{CARTOON_DIR}/man-mirror/{post_id}'
        mkdir(main_dir)
        first_chapter = 1
        max_chapter = 92
        chapters = range(first_chapter, max_chapter + 1)
        for chapter in chapters:
            time_start = process_time()
            self.download_cartoon(post_id, chapter)
            time_end = process_time()
            sleep_time = random.uniform(0.3, 1)
            sleep(sleep_time)
            print(
                f'download post_id: {post_id}\tchapter: {chapter} of {max_chapter}\ttime: {time_end - time_start}(+{sleep_time})')

    def download_cartoon(self, post_id: int, chapter: int) -> None:
        """ download man mirror by post id with page"""
        main_dir = f'{CARTOON_DIR}/man-mirror/{post_id}/chapter-{chapter}'
        mkdir(main_dir)
        page = 0
        is_error = False

        while not is_error:
            try:
                image_path = f'{main_dir}/{page}.png'
                is_file_exists = os.path.isfile(image_path)
                if not is_file_exists:
                    time_start = process_time()
                    image_json = self.__get_json(post_id, chapter, page)
                    image = self.__get_image(post_id, chapter, page)
                    new_image = self.__re_order_images(image, image_json)
                    # old_image_file = Image.fromarray(image)
                    # old_image_file.save(f'{main_dir}/{page}-old.png')

                    new_image_file = Image.fromarray(new_image)
                    new_image_file.save(image_path)
                    time_end = process_time()
                    print(
                        f'download post_id: {post_id}\tchapter: {chapter}\tpage: {page}\ttime: {time_end-time_start}')

                page += 1
            except RequestError:
                is_error = True
            except Exception as error:
                print('loop page error')
                print(error)
                is_error = True

        # if image.status_code == 200:
        # print(image.json())
        #     with open(f'{main_dir}/{page}.png', 'wb') as f:
        #         image.raw.decode_content = True
        #         shutil.copyfileobj(image.raw, f)

    def __get_json(self, post_id: int, chapter: int, page: int) -> ImageJsonShuffle:
        """function for get man mirror json suffer
            example response
            {
                "width": 720,
                "height": 2000,
                "all_row": 4,
                "all_col": 4,
                "shuffles": [14,6,11,8,12,4,3,7,9,1,2,5,10,0,15,13]
            }
        """

        url = f'https://www.manmirror.net/test/{post_id}/{chapter}/{page}.json'
        # print(f'get json {url}')
        response = requests.get(url, timeout=60*1000)
        if (response.status_code == 200):
            data = response.json()
            return ImageJsonShuffle(
                data['width'] or 0,
                data['height'] or 0,
                data['all_row'],
                data['all_col'],
                data['shuffles'],
            )

        # print(response.status_code)
        raise RequestError(
            {"message": 'can get json', "response": response})

    def __get_image(self, post_id: int, chapter: int, page: int) -> np.ndarray:
        """function for get man mirror image"""

        url = f'https://www.manmirror.net/test/{post_id}/{chapter}/{page}.png'
        # print(f'get image {url}')
        response = requests.get(url, timeout=60*1000)
        if (response.status_code == 200):
            response = iio.imread(url)
            return response

        # print(response.status_code)
        raise RequestError(
            {"message": 'can get json', "response": response})

    def __re_order_images(self, image: np.ndarray, image_json: ImageJsonShuffle):
        new_image = np.zeros_like(image)
        # print(f'image.shape: {image.shape}')
        # print(f'new_image.shape: {new_image.shape}')
        # print(f'image_json.shuffles: {image_json.shuffles}')
        for new_row in range(1, image_json.all_row + 1):
            for new_col in range(1, image_json.all_col + 1):
                sort = (new_col - 1) + ((new_row - 1) * image_json.all_row)

                new_top = max((new_row - 1) * image_json.sub_height, 0)
                new_left = max((new_col - 1) * image_json.sub_width, 0)
                new_bottom = min(
                    new_row * image_json.sub_height, image_json.height)
                new_right = min(
                    new_col * image_json.sub_width, image_json.width)
                old_row, old_col = image_json.get_coord_from_index(sort)

                old_top = max((old_row - 1) * image_json.sub_height, 0)
                old_left = max((old_col - 1) * image_json.sub_width, 0)
                old_bottom = min(
                    old_row * image_json.sub_height, image_json.height)
                old_right = min(
                    old_col * image_json.sub_width, image_json.width)
                # print("sort", image_json.shuffles, sort)
                # image_info = {
                #     "sort": sort,
                #     "new_row": new_row,
                #     "new_col": new_col,

                #     "new_top": new_top,
                #     "new_left": new_left,
                #     "new_bottom": new_bottom,
                #     "new_right": new_right,

                #     "old_row": old_row,
                #     "old_col": old_col,

                #     "old_top": old_top,
                #     "old_left": old_left,
                #     "old_bottom": old_bottom,
                #     "old_right": old_right,
                # }
                # print(f'{image_info}')
                # print(json.dumps(image_info, indent=0, ))

                # print('new area')
                # print(new_image[new_left: new_right,
                #                 new_top: new_bottom])
                # print('old area')

                try:
                    sub_image_from_old = image[old_top: old_bottom,
                                               old_left: old_right]
                    new_image[new_top: new_bottom,
                              new_left: new_right] = sub_image_from_old
                except Exception as error:
                    print('error')
                    print(error)
                    print(image[old_top: old_bottom,
                                old_left: old_right])
                # break
            # break
        return new_image
