"""Module providingFunction printing python version."""
import glob
import os
import logging
import shutil
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Tuple
from urllib.parse import unquote

import imageio.v3 as iio
import numpy as np
import requests
from PIL import Image, ImageFile
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

from ..utils.constants import (
    CARTOON_DIR,
    MY_NOVEL,
    MY_NOVEL_APP_KEY,
    MY_NOVEL_HOST,
    LOG_LEVEL,
)
from ..utils.db_client import StealMangaDb
from ..utils.file_helper import mkdir
from ..utils.interface import MangaUploadedToDrive
from ..utils.pdf_helper import merge_images_to_pdf
from ..utils.logging_helper import setup_logging

# sys.path.append("../utils")  # Adds higher directory to python modules path.
# sys.path.append("../../libs")  # Adds higher directory to python modules path.


ImageFile.LOAD_TRUNCATED_IMAGES = True

setup_logging()
logger = logging.getLogger(__name__)

HOST = MY_NOVEL_HOST


class RequestError(Exception):
    """ RequestError """

    def __init__(self, *args: object):
        self.args = args


class MyNovel:
    """ class """
    project_name = MY_NOVEL
    app_key = MY_NOVEL_APP_KEY
    get_info_timeout: int = 30 * 1000
    get_image_timeout: int = 60 * 1000

    def download_cartoons(self, cartoon_id: str, cartoon_name: str, start_ep_index: int = 1, max_workers: int = 4,
                          get_image_timeout: int = 60 * 1000,
                          ) -> None:
        """
        download man mirror by post id
        """
        self.get_image_timeout = get_image_timeout

        start_ep_index = max(start_ep_index, 0)

        product_ep_list_res = self.__get_product_ep_list(cartoon_id)
        product_ep_list = product_ep_list_res['EpTopic']
        logger.info('old len: %s', len(product_ep_list))
        product_ep_list = [d for d in product_ep_list if d is not None and d.get('isPublish')]
        total_ep = len(product_ep_list)
        logger.info('filter len: %s', total_ep)

        steal_manga_db = StealMangaDb()
        steal_manga_db.table_manga_config.update_one({
            'project_name': self.project_name,
            'cartoon_id': cartoon_id
        }, {
            '$set': {
                'max_chapter': total_ep
            }
        })

        main_dir = self.__get_main_dir(cartoon_name)
        mkdir(main_dir)

        logger.info('download %s\ttotal ep: %s', cartoon_name, total_ep)

        start_index = 0
        for i, product_ep in enumerate(product_ep_list):
            if str(start_ep_index) in product_ep['EpName']:
                start_index = i
                break
        product_ep_list_split = product_ep_list[start_index:]

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            for i, product_ep in tqdm(enumerate(product_ep_list_split, start=start_ep_index),
                                      desc=f'Main | {cartoon_name}',
                                      total=len(product_ep_list_split)):

                raw_ep_name = product_ep['EpName'].replace('[', '(').replace(']', ')')
                ep_index = i
                ep_name = raw_ep_name or f'chapter-{ep_index}'
                # continue

                ep_id = product_ep["EpId"]
                ep_dir = self.__get_ep_dir(cartoon_name, ep_name)

                output_pdf_path = f'{main_dir}/{ep_name}.pdf'
                is_file_local_exists = os.path.isfile(output_pdf_path)
                is_file_exists = False

                steal_manga_db = StealMangaDb()
                try:
                    result = steal_manga_db.table_manga_upload.find_one(MangaUploadedToDrive(
                        project_name=self.project_name,
                        cartoon_name=cartoon_name,
                        manga_chapter_name=f'{ep_name}.pdf'
                    ).to_where())
                    is_file_exists = result is not None
                except Exception:
                    is_file_exists = False

                # print(
                #     f'\nexists: {is_file_exists} | {i} | {ep_index} {raw_ep_name} {ep_name}')

                if not is_file_exists and not is_file_local_exists:
                    # Create two threads as follows
                    # self._perform_download_ep(
                    #     product_name, ep_name,
                    #     ep_id, ep_dir, output_pdf_path)
                    pool.submit(self._perform_download_ep,
                                cartoon_name, ep_name,
                                ep_id, ep_dir, output_pdf_path)

            # wait for all tasks to complete
            pool.shutdown(wait=True)

    def _perform_download_ep(self, product_name: str, ep_name: str, ep_id: str, ep_dir: str, output_pdf_path: str):
        mkdir(ep_dir)
        self._download_cartoon_ep(product_name, ep_name, ep_id, ep_dir)
        error, success = self.__merge_to_pdf(ep_dir, output_pdf_path)
        if not success:
            logger.error(
                "__merge_to_pdf error",
                extra={
                    "error": error,
                    "product_name": product_name,
                    "ep_name": ep_name,
                    "ep_dir": ep_dir,
                    "output_pdf_path": output_pdf_path,
                },
            )
        # print(f'output_pdf_path: {output_pdf_path} error: {error}, success: {success}')
        self.__remove_chapter_dir(ep_dir, output_pdf_path)

    def _download_cartoon_ep(self, product_name: str, ep_name: str, ep_id: str, ep_dir: str) -> None:
        """ download man mirror by post id with page"""

        ep_images_res = self.__get_product_ep_images(ep_id)
        ep_image_urls = ep_images_res['ImageUrlLists']

        for index, ep_image_url in tqdm(enumerate(ep_image_urls), total=len(ep_image_urls), desc=f'{product_name} | {ep_name}'):
            page = index + 1
            # print(f'ep_image_url: {page} {ep_image_url}')
            self._download_cartoon_ep_page(
                ep_dir, page, ep_image_url)

    def _download_cartoon_ep_page(self,  ep_dir: str, page: int, ep_image_url: str):
        image_path = f'{ep_dir}/{page}.png'
        is_file_exists = os.path.isfile(image_path)
        if not is_file_exists:
            try:
                image = self.__get_image(ep_image_url)
                # if (image.shape[0] < image.shape[1]):
                #     old_image_file = Image.fromarray(image)
                #     old_image_file.save(f'{main_dir}/{page}-old.png')

                new_image_file = Image.fromarray(image)
                new_image_file.save(image_path)
            except Exception as error:
                logger.error('ep_image_url: %s', ep_image_url)
                logger.error('%s: error %s', image_path, error)
                raise error

    def __merge_to_pdf(self, target_image_dir: str, output_pdf_path: str) -> Tuple[Any, bool]:
        is_file_exists = os.path.isfile(output_pdf_path)
        if not is_file_exists:
            image_paths = glob.glob(
                f'{target_image_dir}/*.png', recursive=False)

            if len(image_paths):
                merge_images_to_pdf(image_paths, output_pdf_path)
                return None, True
            else:
                return 'images to pdf not found', False

        return 'is_file_exists', True

    def __remove_chapter_dir(self, target_image_dir: str, output_pdf_path: str) -> bool:
        is_pdf_exists = os.path.isfile(output_pdf_path)
        is_file_exists = os.path.exists(target_image_dir)
        if is_file_exists and is_pdf_exists:
            shutil.rmtree(target_image_dir, ignore_errors=True)
            return True
        return False

    def __get_main_dir(self, product_name: str) -> str:
        return f'{CARTOON_DIR}/{self.project_name}/{product_name}'

    def __get_ep_dir(self, product_name: str, ep_name: str) -> str:
        main_dir = self.__get_main_dir(product_name)
        return f'{main_dir}/{ep_name}'

    def __get_product_ep_list(self, product_id: str):
        url = f'https://asia-southeast2-mynovel01.cloudfunctions.net/product/{product_id}'
        response = requests.get(url, timeout=self.get_info_timeout)

        if response.status_code == 200:
            data = response.json()
            return data

        # print(response.status_code)
        raise RequestError(
            {"message": 'can get product rp list', "response": response})

    def __get_product_ep_images(self, ep_id: str):
        url = 'https://asia-southeast2-mynovel01.cloudfunctions.net/productEP/getProductEpById'
        response = requests.post(url, {
            "id": ep_id,
            "fontCustom": "Sarabun",
            "appKey": self.app_key,
        }, timeout=self.get_info_timeout)

        if response.status_code == 200:
            data = response.json()
            return data

        # print(response.status_code)
        raise RequestError(
            {"message": 'can get product rp list', "response": response})

    def __get_image(self, ep_image_url: str) -> np.ndarray:
        """function for get man mirror image"""
        ep_image_url = unquote(ep_image_url)
        response = None
        is_firebase_storage = ep_image_url.startswith(
            'https://firebasestorage.googleapis.com')
        is_s3_storage = ep_image_url.startswith('https://manga-store.s3')
        if is_firebase_storage:
            # example https://firebasestorage.googleapis.com/v0/b/mynovel01.appspot.com/o/images/AY3KbqqA1620882955932?alt=media&token=dcb3dbb5-1741-40d0-b8a0-2fe5129d4132
            ep_image_url_only, _ = ep_image_url.split('?', 2)
            image_id = ep_image_url_only.split('/images/')[-1]
            url = f'https://images.mynovel.co/images/{image_id}'

            response = requests.get(url, timeout=self.get_image_timeout, stream=True)
            if response.status_code == 200:
                img = Image.open(response.raw)
                return np.array(img)
        elif is_s3_storage:
            response = requests.get(ep_image_url, timeout=self.get_image_timeout, stream=True)
            if response.status_code == 200:
                img = Image.open(response.raw)
                return np.array(img)
        else:
            try:
                response = requests.get(ep_image_url, timeout=self.get_image_timeout)

                if response.status_code == 200:
                    response = iio.imread(ep_image_url)
                    return response
            except Exception:
                if 'Cartoon/productEP/' in ep_image_url and not ep_image_url.startswith('https://images-manga.mynovel.co'):
                    ep_image_path = ep_image_url.split('/Cartoon/productEP/')[-1]
                    ep_image_url = f'https://images-manga.mynovel.co/file/manga-store/Cartoon/productEP/{ep_image_path}'
                    # print(f'new ep_image_url: {ep_image_url}')
                    response = requests.get(
                        ep_image_url, timeout=self.get_image_timeout, stream=True)

                    if response.status_code == 200:
                        img = Image.open(response.raw)
                        return np.array(img)
                    # print(response.status_code, response.json())

        raise RequestError(
            {"message": 'can get image', "response": response})
