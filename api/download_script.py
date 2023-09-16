""" Main Module """
import getopt
import json
import os
import sys
from time import time
from typing import List

from dotenv import load_dotenv
from libs.man_mirror import ManMirror
from libs.my_novel import MyNovel
from libs.upload_google_drive import generate_drive_manga_exists, upload_to_drive
from libs.upload_google_drive.interface import ManualManMirrorMangaItem
from libs.upload_google_drive.manga_result import get_manga_updated
from libs.utils.constants import MANGA_ROOT_DIR
from libs.utils.db_client import StealMangaDb, get_manga_config
from libs.utils.interface import UpdateMangaConfigData
from pymongo import ReturnDocument

load_dotenv()

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hmond:"

# Long options
long_options = []

MAX_WORKERS = 1


def download_man_mirror_manual() -> None:
    cartoons: List[ManualManMirrorMangaItem] = [
        ManualManMirrorMangaItem(
            cartoon_name="เทพมรณะ",
            cartoon_id="22",
            active=False,
            prefix="GD",
            chapters=["0", "1", "2", "3", "4", "5"]
        ),
        ManualManMirrorMangaItem(
            cartoon_name="ขุนศึก",
            cartoon_id="24",
            active=False,
            prefix="GG",
            chapters=["0", "1", "2", "3", "4", "5", "6"]
        ),
        ManualManMirrorMangaItem(
            cartoon_name="เส้นทางสู่สวรรค์",
            cartoon_id="21",
            active=False,
            prefix="V",
            chapters=["98"] + [str(x) for x in range(106, 110 + 1)]
        ),
        ManualManMirrorMangaItem(
            cartoon_name="L.A.G.",
            cartoon_id="26",
            active=False,
            prefix="LAG%20",
            chapters=[str(x) for x in range(1, 30 + 1)],
            debug=True
        ),
        ManualManMirrorMangaItem(
            cartoon_name="ครูฝึกผู้อ่อนแอ",
            cartoon_id="27",
            active=False,
            prefix="WT",
            chapters=[str(x) for x in range(71, 80 + 1)],
            debug=True
        ),
    ]

    man_mirror = ManMirror()
    generate_drive_manga_exists()

    for cartoon in cartoons:
        cartoon_name: str = cartoon.cartoon_name
        cartoon_id: str = cartoon.cartoon_id
        active: bool = cartoon.active
        prefix: str = cartoon.prefix
        debug: bool = cartoon.debug or False
        chapters: List[str] = cartoon.chapters
        if not active:
            continue

        for chapter in chapters:
            man_mirror.download_manual(
                cartoon_id=cartoon_id,
                cartoon_name=cartoon_name,
                chapter=int(chapter),
                prefix=prefix,
                debug=debug
            )

    upload_to_drive(
        project_name=man_mirror.project_name)


def download_man_mirror():
    man_mirror_cartoons = get_manga_config(ManMirror.project_name)
    # with open(os.path.join(MANGA_ROOT_DIR, 'man-mirror.json'), encoding='utf-8') as f:
    #     man_mirror_cartoons = json.load(f)

    man_mirror = ManMirror()
    generate_drive_manga_exists(target_project_name=man_mirror.project_name)
    for d in man_mirror_cartoons:
        cartoon_name = d.cartoon_name
        cartoon_id = d.cartoon_id
        latest_chapter = d.latest_chapter
        max_chapter = d.max_chapter
        disabled = d.disabled
        print(
            f'\ncartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}\tmax_chapter: {max_chapter}')
        if disabled is None or not disabled:
            man_mirror.download_cartoons(
                cartoon_name=cartoon_name,
                cartoon_id=cartoon_id,
                first_chapter=latest_chapter,
                max_chapter=max_chapter,
                max_workers=MAX_WORKERS
            )
    upload_to_drive(
        project_name=man_mirror.project_name)


def download_my_novel():
    my_novel_cartoons = get_manga_config(MyNovel.project_name)
    # with open(os.path.join(MANGA_ROOT_DIR, 'my-novel.json'), encoding='utf-8') as f:
    #     my_novel_cartoons = json.load(f)

    my_novel = MyNovel()
    generate_drive_manga_exists(target_project_name=my_novel.project_name)
    for d in my_novel_cartoons:
        cartoon_name = d.cartoon_name
        cartoon_id = d.cartoon_id
        latest_chapter = d.latest_chapter
        disabled = d.disabled
        print(
            f'\ncartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}')
        if disabled is None or not disabled:
            my_novel.download_cartoons(cartoon_id, cartoon_name=cartoon_name, start_ep_index=latest_chapter,
                                       max_workers=MAX_WORKERS)
    upload_to_drive(project_name=my_novel.project_name)


def function_execute_time(name: str, cb, **kwargs):
    start_time: float = time()
    cb(**kwargs)
    print(f"\n[Execute Time] {name} | {time() - start_time} seconds")


def execute_download(enable_download_mam_mirror=False,
                     enable_download_mam_mirror_manual=False,
                     enable_download_my_novel=False,
                     debug=False):

    if not enable_download_mam_mirror and not enable_download_mam_mirror_manual and not enable_download_my_novel:
        print('Nothing Download enabled')
        return

    if enable_download_mam_mirror:
        function_execute_time('download_man_mirror', download_man_mirror)

    if enable_download_mam_mirror_manual:
        function_execute_time('download_man_mirror_manual', download_man_mirror_manual)

    if enable_download_my_novel:
        function_execute_time('download_my_novel', download_my_novel)

    print('Download Finished')

    function_execute_time('upload_to_drive all', upload_to_drive)
    print('Upload Finished')

    function_execute_time('generate_drive_manga_exists', generate_drive_manga_exists)
    print('Generate Update Manga Finished')

    function_execute_time('show_manga_updated', get_manga_updated, debug=debug)
    print('END')


def test_db():

    data: list[UpdateMangaConfigData] = []

    my_novel_cartoons = []
    with open(os.path.join(MANGA_ROOT_DIR, 'my-novel.json'), encoding='utf-8') as f:
        my_novel_cartoons = json.load(f)

    for cartoon_name, cartoon_id, latest_chapter, disabled in my_novel_cartoons:
        data.append(UpdateMangaConfigData(
            cartoon_name=cartoon_name,
            cartoon_id=cartoon_id,
            latest_chapter=latest_chapter,
            max_chapter=0,
            disabled=disabled,
            downloaded=0,
            project_name=MyNovel.project_name,
        ))

    man_mirror_cartoons = []
    with open(os.path.join(MANGA_ROOT_DIR, 'man-mirror.json'), encoding='utf-8') as f:
        man_mirror_cartoons = json.load(f)

    for cartoon_name, cartoon_id, latest_chapter, max_chapter, disabled in man_mirror_cartoons:
        data.append(UpdateMangaConfigData(
            cartoon_name=cartoon_name,
            cartoon_id=cartoon_id,
            latest_chapter=latest_chapter,
            max_chapter=max_chapter,
            disabled=disabled,
            downloaded=0,
            project_name=ManMirror.project_name,
        ))

    steal_manga_db = StealMangaDb()
    for d in data:
        steal_manga_db.table_config.find_one_and_update(
            filter={
                "cartoon_id": d.cartoon_id,
            },
            update={
                '$set': d.to_json()
            },
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

    # man_mirror_manga_list =  steal_manga_db.table_config.find({
    #     "project_name": ManMirror.project_name
    # })
    # my_novel_manga_list =  steal_manga_db.table_config.find({
    #     "project_name": MyNovel.project_name
    # })

    # print(f'{ManMirror.project_name} | {[x for x in man_mirror_manga_list]}')


if __name__ == "__main__":
    try:
        debug = False
        enable_download_mam_mirror = False
        enable_download_mam_mirror_manual = False
        enable_download_my_novel = False

        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)

        # checking each argument
        for currentArgument, currentValue in arguments:
            print(f'currentArgument: {currentArgument} | {currentValue}')
            if currentArgument in ("-h", "--Help"):
                print("Displaying Help")
                print("\t -m | enable_download_mam_mirror")
                print("\t -mm | enable_download_mam_mirror_manual")
                print("\t -d | debug")
            elif currentArgument in ("-m"):
                print("Enable Man Mirror")
                enable_download_mam_mirror = True

            elif currentArgument in ("-o"):
                print("Enable Man Mirror Manual")
                enable_download_mam_mirror_manual = True

            elif currentArgument in ("-n"):
                print("Enable My novel")
                enable_download_my_novel = True

            elif currentArgument in ("-d"):
                debug = True
                print("Debug mode")

        function_execute_time('execute download manga', execute_download,
                              enable_download_mam_mirror=enable_download_mam_mirror,
                              enable_download_mam_mirror_manual=enable_download_mam_mirror_manual,
                              enable_download_my_novel=enable_download_my_novel,
                              debug=debug,
                              )

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
