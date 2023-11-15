import re

import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By

from ..utils.constants import MAN_MIRROR
from ..utils.db_client import StealMangaDb


def get_manga_latest_chapter():
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    driver.get("https://www.manmirror.net")
    elements = driver.find_elements(By.CSS_SELECTOR, '#demo > div > div > *')
    steal_manga_db = StealMangaDb()

    for elm in elements:
        latest_chapter_elm = elm.find_element(
            By.CSS_SELECTOR, 'div > div > div > div > div > div > a[href*="chkread.php"]')
        cartoon_name_elm = elm.find_element(
            By.CSS_SELECTOR,  'div > div > a[href*="postId"] > p')

        href = ''
        cartoon_id = ''
        latest_chapter = ''
        cartoon_name = cartoon_name_elm.text or ''

        if latest_chapter_elm:
            href: str | None = latest_chapter_elm.get_attribute('href') or ''

            cartoon_id = re.search(r'(?<=id\=)\d+(?!\&)*', href)
            latest_chapter = re.search(r'(?<=no\=)\d+(?!\&)*', href)
            if cartoon_id:
                cartoon_id = cartoon_id.group()
            if latest_chapter:
                latest_chapter = latest_chapter.group()

        manga_configs = steal_manga_db.table_manga_config.find({
            "cartoon_id": cartoon_id,
            "project_name": MAN_MIRROR,
        }).limit(1).sort("max_chapter", pymongo.DESCENDING)

        manga_config = manga_configs[0]
        if (manga_config):
            # print(manga_config)
            cartoon_name = manga_config['cartoon_name']
            config_max_chapter = int(manga_config['max_chapter'])
            new_latest_chapter = int(latest_chapter or 0)
            is_update = config_max_chapter < new_latest_chapter

            if is_update:
                print(
                    f'cartoon_name: {cartoon_name.strip(): <20}\tis_update: {is_update:<10}\tconfig_max_chapter: {config_max_chapter}\tnew_latest_chapter: {new_latest_chapter}')
        else:
            print(
                f'cartoon_name: {cartoon_name.strip(): <20}\thref: {href:<10}\tmanga_id: {cartoon_id}\tlatest_chapter: {latest_chapter}')

    driver.close()


get_manga_latest_chapter()
