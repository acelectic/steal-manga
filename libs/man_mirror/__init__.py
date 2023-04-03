"""Module providingFunction printing python version."""

import sys
sys.path.append("../utils")  # Adds higher directory to python modules path.
sys.path.append("../../libs")  # Adds higher directory to python modules path.

from .image_json_shuffle import ImageJsonShuffle
import concurrent.futures
from PIL import Image, ImageFile
import numpy as np
import glob
import os
import random
import shutil
from time import process_time, sleep
from typing import Any, Dict, List, Tuple
import requests
import imageio.v3 as iio
from tqdm import tqdm

from libs.utils.constants import CARTOON_DIR
from libs.utils.file_helper import mkdir
from libs.utils.pdf_helper import merge_images_to_pdf
import urllib.parse



ImageFile.LOAD_TRUNCATED_IMAGES = True

HOST = 'https://www.manmirror.net'


class RequestError(Exception):
    """ RequestError """

    def __init__(self, *args: object):
        self.args = args
        
class AppError(Exception):
    """ RequestError """

    def __init__(self, *args: object):
        self.args = args


class ManMirror:
    """ class """
    root = 'man-mirror'

    def download_cartoons(self, cartoon_name: str, post_id: int,  max_chapter: int, first_chapter: int = 1, manga_exists_json: Dict[Any,Any] = {}) -> None:
        """ 
            download man mirror by post id 
        """

        main_dir = self.__get_main_dir(cartoon_name)
        mkdir(main_dir)

        # create a thread pool with 2 threads
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

        chapters = range(first_chapter, (max_chapter or first_chapter) + 1)

        for chapter in tqdm(chapters):

            chapter_dir = self.__get_chapter_dir(cartoon_name, chapter)
            output_pdf_path = f'{main_dir}/{chapter}.pdf'
            is_file_local_exists = os.path.isfile(output_pdf_path)
            is_file_exists = False
            
            try:
                manga_id = manga_exists_json[self.root]["sub_dirs"][cartoon_name]["chapters"][f'{chapter}.pdf']["id"]
                is_file_exists = manga_id is not None
            except: 
                is_file_exists = False
                
            
            if not is_file_exists and not is_file_local_exists:
                pool.submit(self.__perform_download_chapter, cartoon_name, post_id,
                            chapter, chapter_dir, output_pdf_path)
        pool.shutdown(wait=True)

    def __perform_download_chapter(self, cartoon_name: str, post_id: int, chapter: int, chapter_dir: str, output_pdf_path: str):
        some_error = self._download_cartoon_chapter(
            cartoon_name, post_id, chapter)
        self.__merge_to_pdf(
            chapter_dir, output_pdf_path)
        if not some_error:
            self.__remove_chapter_dir(chapter_dir)

    def _download_cartoon_chapter(self, cartoon_name: str, post_id: int, chapter: int) -> bool:
        """ download man mirror by post id with page"""
        main_dir = self.__get_chapter_dir(cartoon_name, chapter)
        mkdir(main_dir)

        max_page = 0
        is_error = False
        is_some_page_error = False
        # print(f'{cartoon_name} chapter {chapter}')
        # print('')

        image_json_list: List[ImageJsonShuffle] = []
        while not is_error:
            try:
                image_json = self.__get_json(post_id, chapter, max_page)
                image_json_list.append(image_json)
                # print(f'get image json page: {max_page}', end='\r')
                max_page += 1
            except RequestError:
                is_error = True
            except Exception as error:
                print('loop get json error')
                print(error)
                is_error = True

        if len(image_json_list) > 0:
            is_some_page_error = self.download_manga_by_image_json(cartoon_name, post_id, chapter, main_dir, max_page, image_json_list)
        else:
            is_some_page_error = self.download_manga_normal(cartoon_name, post_id, chapter, main_dir)
                

        return is_some_page_error

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
            except RequestError as e:
                print(f'request error: {e}')
            except AppError as e:
                print(f'app error: {e}')
            except Exception as error:
                print('loop download_cartoon_chapter_page error')
                print(error)

        return is_some_page_error
    
    def download_manga_normal(self, cartoon_name: str, post_id: int, chapter: int, main_dir: str):
        is_some_page_error = False
        max_page = 200
        pages = range(0, max_page + 1)
        is_error = False
        
        for i, page in tqdm(enumerate(pages), desc=f'{cartoon_name} | chapter {chapter}', total=max_page):
            if is_error:
                break
            try:
                some_error = self._download_cartoon_chapter_page(
                    post_id=post_id, chapter=chapter, main_dir=main_dir, page=page + 1, image_extension='jpg')
                if some_error:
                    is_some_page_error = some_error
            except RequestError as e:
                print(f'request error: {e}')
                is_error = True
            except AppError as e:
                print(f'app error: {e}')
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
            time_start = process_time()
            image = None 
            
            new_image = None
            
            try:
                image = self.__get_image(post_id, chapter, page = str(page), image_extension=image_extension)
            except RequestError:
                raw_page_title = f'หน้า-{str(page).zfill(2)}'.encode('utf-8')
                page_title = urllib.parse.quote_plus(raw_page_title)
                # print(f'raw_page_title: {raw_page_title}\t page_title: {page_title}')
                new_image = self.__get_image(post_id, chapter, page=page_title,  image_extension=image_extension)
            
            
            # if (image.shape[0] < image.shape[1]):
            #     old_image_file = Image.fromarray(image)
            #     old_image_file.save(f'{main_dir}/{page}-old.png')

            if image_json is not None and image is not None:
                new_image, has_some_order_error = self.__re_order_images(
                    image, image_json)
                if has_some_order_error:
                    has_some_error = has_some_order_error
                    old_image_file = Image.fromarray(image)
                    old_image_file.save(f'{main_dir}/{page}-old.png')

            if new_image is not None:
                new_image_file = Image.fromarray(new_image)
                new_image_file.save(image_path)
            
            if new_image is None and image is None:
                has_some_error = True
            time_end = process_time()
            # print(
            #     f'download post_id: {post_id}\tchapter: {chapter}\tpage: {page}\ttime: {time_end-time_start}')
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

    def __get_main_dir(self, post_id: str) -> str:
        return f'{CARTOON_DIR}/{self.root}/{post_id}'

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
        response = requests.get(url, timeout=5*1000)
        if (response.status_code == 200):
            data = response.json()
            # print(f'data json {data}')
            return ImageJsonShuffle(
                data['width'] or 0,
                data['height'] or 0,
                data['all_row'],
                data['all_col'],
                data['shuffles'],
            )

        # print(response.status_code)
        raise RequestError(
            {"message": 'can not get json', "response": response})

    def __get_image(self, post_id: int, chapter: int, page: str, image_extension: str = 'png') -> np.ndarray:
        """function for get man mirror image"""
        url = f'https://www.manmirror.net/test/{post_id}/{chapter}/{page}.{image_extension}'
        if image_extension == 'jpg':
            # print(f'get image {url}')
            response = requests.get(url, timeout=20*1000, stream=True)
            if response.status_code == 200:
                img = Image.open(response.raw)
                return np.array(img)
            
        else:
            response = requests.get(url, timeout=20*1000)
            if (response.status_code == 200):
                response = iio.imread(url)
                return response
        
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
                    print('error')
                    print(error)
                    print(f'{image_info}')
                    print({
                        "old_top": old_top,
                        "old_bottom": old_bottom,
                        "old_left": old_left,
                        "old_right": old_right
                    })
                    print(f'image.shape: {image.shape}')
                    print(f'new_image.shape: {new_image.shape}')
                    print(f'image_json.shuffles: {image_json.shuffles}')
                    raise AppError({
                        "message": "re_order_images error",
                        "error": error                    
                    })
                # break
            # break
        return new_image, has_some_error
