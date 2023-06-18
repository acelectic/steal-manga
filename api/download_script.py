""" Main Module """
import json
import os
from time import time
from typing import List

from dotenv import load_dotenv
from libs.man_mirror import ManMirror
from libs.my_novel import MyNovel
from libs.upload_google_drive import generate_drive_manga_exists, upload_to_drive
from libs.upload_google_drive.interface import ManualManMirrorMangaItem
from libs.upload_google_drive.manga_result import get_manga_updated
from libs.utils.constants import MANGE_ROOT_DIR

load_dotenv()

MAX_WORKERS = 2


def download_man_mirror_manual() -> None:
    cartoons: list[ManualManMirrorMangaItem] = [
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
            active=True,
            prefix="GG",
            chapters=["0", "1", "2", "3", "4", "5", "6"]
        ),
    ]

    man_mirror = ManMirror()
    manga_exists_json = generate_drive_manga_exists(force_update=True)

    for cartoon in cartoons:
        cartoon_name = cartoon.cartoon_name
        cartoon_id = cartoon.cartoon_id
        active = cartoon.active
        prefix = cartoon.prefix
        chapters: List[str] = cartoon.chapters
        if not active:
            continue

        for chapter in chapters:
            man_mirror.download_manual(
                cartoon_id=cartoon_id,
                cartoon_name=cartoon_name,
                chapter=int(chapter),
                prefix=prefix,
                manga_exists_json=manga_exists_json,
            )

    upload_to_drive(
        project_name=man_mirror.root)


def download_man_mirror():
    man_mirror_cartoons = []
    with open(os.path.join(MANGE_ROOT_DIR, 'man-mirror.json'), encoding='utf-8') as f:
        man_mirror_cartoons = json.load(f)

    man_mirror = ManMirror()
    manga_exists_json = generate_drive_manga_exists(
        force_update=True, project_name=man_mirror.root)
    for cartoon_name, cartoon_id, latest_chapter, max_chapter, disabled in man_mirror_cartoons:
        print(
            f'\ncartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}\tmax_chapter: {max_chapter}')
        if disabled is None or not disabled:
            man_mirror.download_cartoons(
                cartoon_name,
                cartoon_id,
                first_chapter=latest_chapter,
                max_chapter=max_chapter,
                manga_exists_json=manga_exists_json,
                max_workers=MAX_WORKERS
            )
    upload_to_drive(
        project_name=man_mirror.root)


def download_my_novel():
    my_novel_cartoons = []
    with open(os.path.join(MANGE_ROOT_DIR, 'my-novel.json'), encoding='utf-8') as f:
        my_novel_cartoons = json.load(f)

    my_novel = MyNovel()
    manga_exists_json = generate_drive_manga_exists(
        force_update=True,  project_name=my_novel.root)
    for cartoon_name, cartoon_id, latest_chapter, disabled in my_novel_cartoons:
        print(
            f'\ncartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}')
        if disabled is None or not disabled:
            my_novel.download_cartoons(cartoon_id, start_ep_index=latest_chapter,
                                       manga_exists_json=manga_exists_json, max_workers=MAX_WORKERS)
    upload_to_drive(project_name=my_novel.root)


def function_execute_time(name: str, cb, **kwargs):
    start_time: float = time()
    cb(**kwargs)
    print(f"\n[Execute Time] {name} | {time() - start_time} seconds")


def execute_download(enable_download_mam_mirror=False,
                     enable_download_mam_mirror_manual=False,
                     enable_download_my_novel=False,
                     debug=False):

    # manga_exists_json = generate_drive_manga_exists(force_update=True, logging=False)
    # generate_drive_manga_exists(force_update=True)
    # function_execute_time('show_manga_updated',show_manga_updated)
    # return
    if not enable_download_mam_mirror and not enable_download_mam_mirror_manual and not enable_download_my_novel:
        return

    def tmp_x() -> None:
        generate_drive_manga_exists(force_update=True)

    # function_execute_time('generate_drive_manga_exists', tmp_x)

    # function_execute_time('upload_to_drive all', upload_to_drive)

    # function_execute_time('generate_drive_manga_exists', tmp_x)

    if enable_download_mam_mirror:
        function_execute_time('download_man_mirror', download_man_mirror)

    if enable_download_mam_mirror_manual:
        function_execute_time('download_man_mirror_manual',
                              download_man_mirror_manual)

    if enable_download_my_novel:
        function_execute_time('download_my_novel', download_my_novel)

    print('Download Finished')

    function_execute_time('upload_to_drive all', upload_to_drive)
    print('Upload Finished')

    function_execute_time('generate_drive_manga_exists', tmp_x)
    print('Generate Update Manga Finished')

    function_execute_time('show_manga_updated', get_manga_updated, debug=debug)
    print('END')


if __name__ == "__main__":
    function_execute_time('execute download manga', execute_download,
                          enable_download_mam_mirror=True,
                          enable_download_mam_mirror_manual=False,
                          enable_download_my_novel=True,
                          debug=True,
                          )
