"""Module providingFunction printing python version."""
from concurrent.futures import ThreadPoolExecutor
import glob
import os
import shutil
from typing import Any, List, Tuple
from urllib.parse import unquote

import imageio.v3 as iio
import numpy as np
import requests
from PIL import Image, ImageFile
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

from utils.constants import CARTOON_DIR
from utils.file_helper import mkdir
from utils.pdf_helper import merge_images_to_pdf

ImageFile.LOAD_TRUNCATED_IMAGES = True

HOST = 'https://www.manmirror.net'


class RequestError(Exception):
    """ RequestError """

    def __init__(self, *args: object):
        self.args = args


class MyNovel:
    """ class """
    root = 'my-novel'
    app_key = "xdde8cNN5k7AuVTMgz7b"

    def download_cartoons(self, product_id: str, start_ep_index: int = 1) -> None:
        """
        download man mirror by post id
        """
        start_ep_index = max(start_ep_index, 0)

        product_ep_list_res = self.__get_product_ep_list(product_id)
        product_ep_list = product_ep_list_res['EpTopic']
        print(f'old len: {len(product_ep_list)}')
        product_ep_list = list(
            filter(lambda x: x is not None, product_ep_list))
        total_ep = len(product_ep_list)
        print(f'filter len: {total_ep}')

        product_name = product_ep_list_res['ProductName']

        main_dir = self.__get_main_dir(product_name)
        mkdir(main_dir)

        print(f'download {product_name}\ttotal ep: {total_ep}')

        def sub_process(args):
            i, product_ep = args
            ep_index = i + 1
            ep_id = product_ep["EpId"]
            ep_name = f'chapter-{ep_index}'
            ep_dir = self.__get_ep_dir(product_name, ep_name)

            output_pdf_path = f'{main_dir}/{ep_name}.pdf'
            is_file_exists = os.path.isfile(output_pdf_path)

            if not is_file_exists:
                # Create two threads as follows
                self._perform_download_ep(
                    product_name, ep_name,
                    ep_id, ep_dir, output_pdf_path)

        # thread_map(sub_process, enumerate(product_ep_list),
        #            desc=f'{product_name}',
        #            tqdm_class=tqdm,
        #            total=len(product_ep_list),
        #            max_workers=2)

        # create a thread pool with 2 threads
        with ThreadPoolExecutor(max_workers=2) as pool:
            # tqdm(pool.map(sub_process, enumerate(
            #     product_ep_list)),
            #     desc=f'{product_name}',
            #     total=len(product_ep_list))

            start_index = 0
            for i, product_ep in enumerate(product_ep_list):
                if str(start_ep_index) in product_ep['EpName']:
                    start_index = i
                    break

            product_ep_list_split = product_ep_list[start_index:]
            # print(
            #     f'{len(product_ep_list)} {len(product_ep_list_split)} {start_index} {start_ep_index}')

            for i, product_ep in tqdm(enumerate(product_ep_list_split, start=start_ep_index),
                                      desc=f'{product_name}',
                                      total=len(product_ep_list_split)):
                raw_ep_name = product_ep['EpName']
                ep_index = i
                ep_name = raw_ep_name or f'chapter-{ep_index}'
                # continue

                ep_id = product_ep["EpId"]
                ep_dir = self.__get_ep_dir(product_name, ep_name)

                output_pdf_path = f'{main_dir}/{ep_name}.pdf'
                is_file_exists = os.path.isfile(output_pdf_path)

                print(
                    f'\nexists: {is_file_exists} | {i} | {ep_index} {raw_ep_name} {ep_name}')

                if not is_file_exists:
                    # Create two threads as follows
                    # self._perform_download_ep(
                    #     product_name, ep_name,
                    #     ep_id, ep_dir, output_pdf_path)
                    pool.submit(self._perform_download_ep,
                                product_name, ep_name,
                                ep_id, ep_dir, output_pdf_path)

            # wait for all tasks to complete
            pool.shutdown(wait=True)

    def _perform_download_ep(self, product_name: str, ep_name: str, ep_id: str, ep_dir: str, output_pdf_path: str):
        mkdir(ep_dir)
        self._download_cartoon_ep(product_name, ep_name, ep_id, ep_dir)
        self.__merge_to_pdf(ep_dir, output_pdf_path)
        self.__remove_chapter_dir(ep_dir)

    def _download_cartoon_ep(self, product_name: str, ep_name: str, ep_id: str, ep_dir: str) -> None:
        """ download man mirror by post id with page"""

        ep_images_res = self.__get_product_ep_images(ep_id)
        ep_image_urls = ep_images_res['ImageUrlLists']

        for index, ep_image_url in tqdm(enumerate(ep_image_urls), total=len(ep_image_urls), desc=f'{product_name} | {ep_name}'):
            page = index + 1
            self._download_cartoon_ep_page(
                ep_dir, page, ep_image_url)

    def _download_cartoon_ep_page(self,  ep_dir: str, page: int, ep_image_url: str):
        image_path = f'{ep_dir}/{page}.png'
        is_file_exists = os.path.isfile(image_path)
        if not is_file_exists:
            image = self.__get_image(ep_image_url)
            # if (image.shape[0] < image.shape[1]):
            #     old_image_file = Image.fromarray(image)
            #     old_image_file.save(f'{main_dir}/{page}-old.png')

            new_image_file = Image.fromarray(image)
            new_image_file.save(image_path)

    def __merge_to_pdf(self, target_image_dir: str, output_pdf_path: str) -> Tuple[Any, bool]:
        is_file_exists = os.path.isfile(output_pdf_path)
        if not is_file_exists:
            image_paths = glob.glob(
                f'{target_image_dir}/*.png', recursive=False)
            merge_images_to_pdf(image_paths, output_pdf_path)
            return None, True

        return 'is_file_exists', False

    def __remove_chapter_dir(self, target_image_dir: str) -> bool:
        is_file_exists = os.path.exists(target_image_dir)
        if is_file_exists:
            shutil.rmtree(target_image_dir, ignore_errors=True)
            return True
        return False

    def __get_main_dir(self, product_name: str) -> str:
        return f'{CARTOON_DIR}/{self.root}/{product_name}'

    def __get_ep_dir(self, product_name: str, ep_name: str) -> str:
        main_dir = self.__get_main_dir(product_name)
        return f'{main_dir}/{ep_name}'

    def __get_product_ep_list(self, product_id: str):
        url = f'https://asia-southeast2-mynovel01.cloudfunctions.net/product/{product_id}'
        response = requests.get(url, timeout=15 * 1000)

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
        }, timeout=15 * 1000)

        if response.status_code == 200:
            data = response.json()
            return data

        # print(response.status_code)
        raise RequestError(
            {"message": 'can get product rp list', "response": response})

    def __get_image(self, ep_image_url: str) -> np.ndarray:
        """function for get man mirror image"""
        ep_image_url = unquote(ep_image_url)

        is_firebase_storage = ep_image_url.startswith(
            'https://firebasestorage.googleapis.com')
        if is_firebase_storage:
            """
                https://firebasestorage.googleapis.com/v0/b/mynovel01.appspot.com/o/images/AY3KbqqA1620882955932?alt=media&token=dcb3dbb5-1741-40d0-b8a0-2fe5129d4132
            """
            ep_image_url_only, _ = ep_image_url.split('?', 2)
            image_id = ep_image_url_only.split('/images/')[-1]
            url = f'https://images.mynovel.co/images/{image_id}'

            response = requests.get(url, timeout=60*1000, stream=True)
            if response.status_code == 200:
                img = Image.open(response.raw)
                return np.array(img)
        else:
            response = requests.get(ep_image_url, timeout=60*1000)

            if response.status_code == 200:
                response = iio.imread(ep_image_url)
                return response

        print(response.json())
        raise RequestError(
            {"message": 'can get image', "response": response})
