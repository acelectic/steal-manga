"""Module providingFunction printing python version."""

import concurrent.futures
import glob
import json
import os
import random
import shutil
import sys
import urllib.parse
from pprint import pprint
from time import process_time, sleep
from typing import Any, Dict, List, Tuple

import imageio.v3 as iio
import numpy as np
import requests
from PIL import Image, ImageFile
from tqdm import tqdm

from ..utils.constants import CARTOON_DIR
from ..utils.file_helper import mkdir
from ..utils.pdf_helper import merge_images_to_pdf
from .image_json_shuffle import ImageJsonShuffle

# sys.path.append("../utils")  # Adds higher directory to python modules path.
# sys.path.append("../../libs")  # Adds higher directory to python modules path.

ImageFile.LOAD_TRUNCATED_IMAGES = True

HOST = 'https://www.manmirror.net'


class RequestError(Exception):
    """ RequestError """

    def __init__(self, *args: object):
        self.args = args


class RequestErrorMustDebug(Exception):
    """ RequestError """
    data: object = None

    def __init__(self, data: object, image_json: ImageJsonShuffle, *args: object):
        self.args = args
        self.data = data
        self.image_json: ImageJsonShuffle = image_json


class AppError(Exception):
    """ RequestError """

    def __init__(self, *args: object):
        self.args = args


class ManMirror:
    """ class """
    root: str = 'man-mirror'
    get_json_timeout: int = 10 * 1000
    get_image_timeout: int = 60 * 1000

    def download_cartoons(self, cartoon_name: str, post_id: int,  max_chapter: int, manga_exists_json: Dict[Any, Any],  first_chapter: int = 1, max_workers: int = 4,
                          get_json_timeout: int = 10 * 1000,
                          get_image_timeout: int = 60 * 1000,
                          ) -> None:
        """ 
            download man mirror by post id 
        """
        self.get_json_timeout: int = get_json_timeout
        self.get_image_timeout: int = get_image_timeout

        main_dir = self.__get_main_dir(cartoon_name)
        mkdir(main_dir)

        # create a thread pool with 2 threads
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

        chapters = range(first_chapter, (max_chapter or first_chapter) + 1)

        for chapter in tqdm(chapters):

            chapter_dir = self.__get_chapter_dir(cartoon_name, chapter)
            output_pdf_path = f'{main_dir}/{chapter}.pdf'
            is_file_local_exists = os.path.isfile(output_pdf_path)
            is_file_exists = False

            try:
                manga_id = manga_exists_json[self.root]["sub_dirs"][
                    cartoon_name]["chapters"][f'{chapter}.pdf']["id"]
                is_file_exists = manga_id is not None
            except Exception:
                is_file_exists = False

            if not is_file_exists and not is_file_local_exists:
                pool.submit(self.__perform_download_chapter, cartoon_name, post_id,
                            chapter, chapter_dir, output_pdf_path)
        pool.shutdown(wait=True)

    def __perform_download_chapter(self, cartoon_name: str, post_id: int, chapter: int, chapter_dir: str, output_pdf_path: str):
        some_error, is_some_json_error = self._download_cartoon_chapter(
            cartoon_name, post_id, chapter)
        if not is_some_json_error:
            self.__merge_to_pdf(
                chapter_dir, output_pdf_path)
        if not some_error and not is_some_json_error:
            self.__remove_chapter_dir(chapter_dir)

    def _download_cartoon_chapter(self, cartoon_name: str, post_id: int, chapter: int) -> Tuple[bool, bool]:
        """ download man mirror by post id with page"""
        chapter_dir = self.__get_chapter_dir(cartoon_name, chapter)
        mkdir(chapter_dir)

        max_page = 0
        is_error = False
        is_some_page_error = False
        is_some_json_error = False
        # print(f'{cartoon_name} chapter {chapter}')
        # print('')

        image_json_list: List[ImageJsonShuffle] = []
        while not is_error:
            try:
                image_json: ImageJsonShuffle = self.__get_json(post_id, chapter, max_page)
                image_json_list.append(image_json)
                if image_json.must_debug:
                    is_some_json_error = True
                    with open(os.path.join(chapter_dir, 'error.txt'), '+a', encoding='utf-8') as error_file:
                        debug_info = json.dumps({
                            "is_shuffles_not_match": image_json.is_shuffles_not_match,
                            "is_shuffles_radio_size_too_many": image_json.is_shuffles_radio_size_too_many,
                            "is_shuffles_size_too_many": image_json.is_shuffles_size_too_many
                        })
                        error_file.write(f'{max_page} {debug_info}\n')
                    if image_json.raw:
                        with open(os.path.join(chapter_dir, f'{max_page}.json'), 'w', encoding='utf-8') as error_file:
                            error_file.write(json.dumps(image_json.raw))
                # print(f'get image json page: {max_page}', end='\r')
                max_page += 1

            except RequestErrorMustDebug as error:
                is_error = True
            except RequestError:
                is_error = True
            except Exception as error:
                print('loop get json error')
                print(error)
                is_error = True

        if len(image_json_list) > 0:
            is_some_page_error = self.download_manga_by_image_json(
                cartoon_name, post_id, chapter, chapter_dir, max_page, image_json_list)
        else:
            is_some_page_error = self.download_manga_normal(
                cartoon_name, post_id, chapter, chapter_dir)

        return is_some_page_error, is_some_json_error

    def download_manga_by_image_json(self, cartoon_name: str, post_id: int, chapter: int, main_dir: str, max_page: int, image_json_list: List[ImageJsonShuffle]):
        is_some_page_error = False
        pages = range(0, max_page + 1)

        for i, page in tqdm(enumerate(pages), desc=f'{cartoon_name} | chapter {chapter}', total=max_page):
            try:
                image_json = None
                if len(image_json_list) - 1 >= i:
                    image_json = image_json_list[i]

                some_error = self._download_cartoon_chapter_page(
                    post_id=post_id, chapter=chapter, main_dir=main_dir, page=page, image_json=image_json)
                if some_error:
                    is_some_page_error = some_error
            except RequestError:
                # print(f'request error: {e}')
                continue
            except AppError as error:
                print(f'app error: {error}')
            except Exception as error:
                print('loop download_cartoon_chapter_page error')
                print(error)

        return is_some_page_error

    def download_manga_normal(self, cartoon_name: str, post_id: int, chapter: int, main_dir: str):
        is_some_page_error = False
        max_page = 200
        pages = range(0, max_page + 1)
        is_error = False

        for page in tqdm(pages, desc=f'{cartoon_name} | chapter {chapter}', total=max_page):
            if is_error:
                break
            try:
                some_error = self._download_cartoon_chapter_page(
                    post_id=post_id, chapter=chapter, main_dir=main_dir, page=page + 1, image_extension='jpg')
                if some_error:
                    is_some_page_error = some_error
            except RequestError:
                # print(f'request error: {e}')
                is_error = True
                continue
            except AppError as error:
                print(f'app error: {error}')
                is_error = True
            except Exception as error:
                print('loop download_cartoon_chapter_page error')
                print(error)
                is_error = True

        return is_some_page_error

    def _download_cartoon_chapter_page(self, post_id: int, chapter: int, main_dir: str, page: int, image_json: ImageJsonShuffle | None = None, image_extension: str = 'png'):
        image_path = f'{main_dir}/{page}.png'
        is_file_exists = os.path.isfile(image_path)
        has_some_error = False
        if not is_file_exists:
            image = None
            new_image = None

            try:
                image = self.__get_image(post_id, chapter, page=str(page))
            except RequestError:
                raw_page_title = f'หน้า-{str(page).zfill(2)}'.encode('utf-8')
                page_title = urllib.parse.quote_plus(raw_page_title)
                # print(f'raw_page_title: {raw_page_title}\t page_title: {page_title}')
                new_image = self.__get_image(
                    post_id, chapter, page=page_title,  image_extension=image_extension)

            # if (image.shape[0] < image.shape[1]):
            #     old_image_file = Image.fromarray(image)
            #     old_image_file.save(f'{main_dir}/{page}-old.png')

            if image_json is not None and image is not None:

                # if image_json.must_debug:
                #     old_image_file = Image.fromarray(image)
                #     old_image_file.save(f'{main_dir}/{page}-debug.png')
                # else:
                #     new_image, has_some_order_error = self.__re_order_images(
                #         image, image_json)
                #     if has_some_order_error:
                #         has_some_error = has_some_order_error
                #         old_image_file = Image.fromarray(image)
                #         old_image_file.save(f'{main_dir}/{page}-before-order.png')
                new_image, has_some_order_error = self.__re_order_images(
                    image, image_json)
                if has_some_order_error:
                    has_some_error = has_some_order_error
                    old_image_file = Image.fromarray(image)
                    old_image_file.save(f'{main_dir}/{page}-before-order.png')

            if new_image is not None:
                new_image_file = Image.fromarray(new_image)
                new_image_file.save(image_path)

            if new_image is None and image is None:
                has_some_error = True
        return has_some_error

    def __merge_to_pdf(self, target_image_dir: str, output_pdf_path: str) -> Tuple[str, bool]:
        is_file_exists = os.path.isfile(output_pdf_path)
        extensions = ('*.png', '*.jpg')
        if not is_file_exists:
            image_paths = []

            for ext in extensions:
                image_paths.extend(glob.glob(f'{target_image_dir}/{ext}', recursive=False))

            if len(image_paths) > 0:
                merge_images_to_pdf(image_paths, output_pdf_path)
            return '', True

        return 'is_file_exists', False

    def __remove_chapter_dir(self, target_image_dir: str) -> bool:
        is_file_exists = os.path.exists(target_image_dir)
        if is_file_exists:
            shutil.rmtree(target_image_dir, ignore_errors=True)
            return True
        return False

    def __get_main_dir(self, cartoon_name: str) -> str:
        return f'{CARTOON_DIR}/{self.root}/{cartoon_name}'

    def __get_chapter_dir(self, cartoon_name: str, chapter: int) -> str:
        main_dir = self.__get_main_dir(cartoon_name)
        return f'{main_dir}/chapter-{chapter}'

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
        response = requests.get(url, timeout=self.get_json_timeout)
        if response.status_code == 200:
            data = response.json()
            width = data['width'] or 0
            height = data['height'] or 0
            all_row = data['all_row']
            all_col = data['all_col']
            shuffles = data['shuffles']
            image_json_result = ImageJsonShuffle(
                width=width,
                height=height,
                all_row=all_row,
                all_col=all_col,
                shuffles=shuffles,
                raw=data
            )
            if width == 0 or height == 0:
                message = 'width or height null'
                # print(message)
                raise RequestError(
                    {"message": message, "response": response})

            # if image_json_result.must_debug:
            #     message = f'shuffles size is too many [{len(shuffles)}] '
            #     # print(message)
            #     raise RequestErrorMustDebug(
            #         data,
            #         image_json_result,
            #         {"message": message, "response": response},
            #     )

            # print(f'data json {data}')
            return image_json_result

        # print(response.status_code)
        raise RequestError(
            {"message": 'can not get json', "response": response})

    def __get_image(self, post_id: int, chapter: int, page: str, image_extension: str = 'png') -> np.ndarray:
        """function for get man mirror image"""
        url = f'https://www.manmirror.net/test/{post_id}/{chapter}/{page}.{image_extension}'
        if image_extension == 'jpg':
            # print(f'get image {url}')
            response = requests.get(url, timeout=self.get_image_timeout, stream=True)
            if response.status_code == 200:
                img = Image.open(response.raw)
                return np.array(img)
            elif response.status_code == 404:
                # print(f'url: {url}')
                pass
        else:
            response = requests.get(url, timeout=self.get_image_timeout)
            if response.status_code == 200:
                response = iio.imread(url)
                return response
            elif response.status_code == 404:
                # print(f'url: {url}')
                pass

        # if image_extension == 'jpg':
        #     print(f'url: {url}')
        #     print(response.status_code)
        #     print(response.json())

        # print(f'get image {url}')
        raise RequestError(
            {"message": 'can not get image', "response": response})

    def __re_order_images(self, image: np.ndarray, image_json: ImageJsonShuffle):
        has_some_error = False
        new_image = np.zeros_like(image)
        if image_json.must_debug:
            pprint(image_json)
        # print(f'image.shape: {image.shape}')
        # print(f'new_image.shape: {new_image.shape}')
        # print(f'image_json.shuffles: {image_json.shuffles}')
        for new_row in range(1, image_json.all_row + 1):
            for new_col in range(1, image_json.all_col + 1):
                sort = (new_col - 1) + ((new_row - 1) * image_json.all_col)

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
                image_info = {
                    "sort": sort,
                    "new_row": new_row,
                    "new_col": new_col,

                    "new_top": new_top,
                    "new_left": new_left,
                    "new_bottom": new_bottom,
                    "new_right": new_right,

                    "old_row": old_row,
                    "old_col": old_col,

                    "old_top": old_top,
                    "old_left": old_left,
                    "old_bottom": old_bottom,
                    "old_right": old_right,

                    "sub_height": image_json.sub_height,
                    "sub_width": image_json.sub_width,
                    "all_col": image_json.all_col,
                    "all_row": image_json.all_row,
                }
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
                    has_some_error = True
                    # sub_image_from_old = image[old_top: old_bottom,
                    #                            old_left: old_right]
                    # sub_image_from_target = new_image[new_top: new_bottom,
                    #                                   new_left: new_right]
                    # print('sub_image_from_old')
                    # print(sub_image_from_old)
                    # print('sub_image_from_target')
                    # print(sub_image_from_target)

                    print('error')
                    print('error')
                    print('error')
                    print(error)
                    pprint(image_info, indent=2)
                    print({
                        "old_top": old_top,
                        "old_bottom": old_bottom,
                        "old_left": old_left,
                        "old_right": old_right
                    })
                    print(f'image.shape: {image.shape}')
                    print(f'new_image.shape: {new_image.shape}')
                    # print(
                    #     f'image_json.shuffles: {image_json.shuffles} [{len(image_json.shuffles)}]')
                    # print(f'image_json.must_debug: {image_json.must_debug}')
                    raise AppError({
                        "message": "re_order_images error",
                        "error": error
                    }) from error
                # break
            # break
        return new_image, has_some_error

    def download_manual(self, cartoon_name: str, cartoon_id: str, chapter: int, manga_exists_json: Dict[Any, Any], prefix: str, debug=False):
        main_dir = self.__get_main_dir(cartoon_name)
        chapter_dir = self.__get_chapter_dir(cartoon_name, chapter)
        mkdir(chapter_dir)
        output_pdf_path = f'{main_dir}/{chapter}.pdf'
        is_file_local_exists = os.path.exists(output_pdf_path)
        is_file_exists = False
        try:
            manga_id = manga_exists_json[self.root]["sub_dirs"][
                cartoon_name]["chapters"][f'{chapter}.pdf']["id"]
            is_file_exists = manga_id is not None
        except Exception:
            is_file_exists = False

        if is_file_exists or is_file_local_exists:
            return

        loop_target: List[Tuple[int, int]] = []
        for d1 in range(10):
            for d2 in range(25):
                loop_target.append((d1, d2))

        count_error_continue = 0
        d1_error = None
        for i, d in tqdm(enumerate(loop_target), desc=f'cartoon_name {cartoon_name}[{chapter}]', total=len(loop_target)):
            d1, d2 = d
            page = i + 1
            image_path = f'{chapter_dir}/{page}.png'
            file_with_prefix = f'{prefix}{ str(chapter).zfill(2)}-{d1}_{ str(d2).zfill(3) }'
            if prefix == 'V':
                file_with_prefix = f'{prefix}{d1}_{ str(d2).zfill(3) }'

            image_url = f'https://www.manmirror.net/test/{cartoon_id}/{chapter}/{file_with_prefix}.jpg'

            if os.path.exists(image_path):
                continue

            if d1_error is not None and d1_error <= d1:
                continue

            if count_error_continue > 4:
                break

            try:
                if debug:
                    print(f'image_url: {image_url}')
                new_image = self.call_get_image(image_url)
                if new_image is not None:
                    new_image_file = Image.fromarray(new_image)
                    new_image_file.save(image_path)
                count_error_continue = 0
            except Exception as e:
                if debug:
                    print(f'image_url: {image_url}')
                    print(e)
                d1_error = d1
                count_error_continue += 1
                continue

        self.__merge_to_pdf(chapter_dir, output_pdf_path)
        self.__remove_chapter_dir(chapter_dir)

    def call_get_image(self, url):
        response = requests.get(url, timeout=self.get_image_timeout, stream=True)
        if response.status_code == 200:
            img = Image.open(response.raw)
            return np.array(img)
