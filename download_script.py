""" Main Module """
from time import time
from typing import List

from dotenv import load_dotenv

from libs.man_mirror import ManMirror
from libs.my_novel import MyNovel
from libs.upload_google_drive import generate_drive_manga_exists, upload_to_drive
from libs.upload_google_drive.interface import ManualManMirrorMangaItem
from libs.upload_google_drive.manga_result import show_manga_updated

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
    man_mirror_cartoons = [
        ['เลเวลอัพไม่จำกัด', 1, 138, 149],
        ['สุดยอดจอมยุทธ', 7, 1, 118],
        ['ดาบวายุอัสนี', 19, 21, 75],
        ['จ้าวสงคราม', 3, 65, 135],
        ['มือกระบี่ไร้พ่าย', 5, 100, 162],
        # ['จิตวิญญาณวายุ', 16, 1, 76],
        # ['โกแซม นักรบในตำนาน', 12, 65, 66],
        ['บัณฑิตหวนคืน', 8, 1, 146],  # max 133
        ['เส้นทางสู่สวรรค์', 21, 35, 80],
        ['มังกรพิษ', 6, 120, 133],
        # ['หนึ่งในใต้หล้า', 10, 1, 111],  # max 100
        ['ตำนานกระบี่อุดร', 9, 150, 157],
        ['เทพมรณะ', 22, 1, 41],
        # ['เทพอัสนี', 11, 1, 141],
        ['ทายาทจอมมาร', 2, 1, 84],
        ['ทายาทเทพธนู', 20, 1, 50],
        ['ขุนศึก', 24, 30, 61],
        ['เมื่อผมดันหยิบมือถือจากโลกอื่น', 23, 1, 50]
    ]

    man_mirror = ManMirror()
    manga_exists_json = generate_drive_manga_exists(
        force_update=True, project_name=man_mirror.root)
    for cartoon_name, cartoon_id, latest_chapter, max_chapter in man_mirror_cartoons:
        print(
            f'\ncartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}\tmax_chapter: {max_chapter}')

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
    my_novel_cartoons = [
        # ['Against the Gods - อสูรพลิกฟ้า', '6EvFPzipwmnKxlZMqhjs', 423],
        ['Cultivator vs Superhero (ทันจีน)', '6yeQcr6kL14A96eUwKZA', 250],
        ['Tales of Demon and Gods', 'E8XDEk8Dv9vbchSGtF5n', 419],
        ['Infinite Mage', '63b2a71156baafb4e8213126', 1]
    ]
    my_novel = MyNovel()
    manga_exists_json = generate_drive_manga_exists(
        force_update=True,  project_name=my_novel.root)
    for cartoon_name, cartoon_id, latest_chapter in my_novel_cartoons:

        print(
            f'\ncartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}')
        my_novel.download_cartoons(cartoon_id, start_ep_index=latest_chapter,
                                   manga_exists_json=manga_exists_json, max_workers=MAX_WORKERS)
    upload_to_drive(project_name=my_novel.root)


def function_execute_time(name: str, cb):
    start_time: float = time()
    cb()
    print(f"\n[Execute Time] {name} | {time() - start_time} seconds")


def run():
    ENABLE_DOWNLOAD_MAM_MIRROR = True
    ENABLE_DOWNLOAD_MAM_MIRROR_MANUAL = False
    ENABLE_DOWNLOAD_MY_NOVEL = True
    # manga_exists_json = generate_drive_manga_exists(force_update=True, logging=False)
    # generate_drive_manga_exists(force_update=True)
    # function_execute_time('show_manga_updated',show_manga_updated)
    # return

    if ENABLE_DOWNLOAD_MAM_MIRROR:
        function_execute_time('download_man_mirror', download_man_mirror)

    if ENABLE_DOWNLOAD_MAM_MIRROR_MANUAL:
        function_execute_time('download_man_mirror_manual',
                              download_man_mirror_manual)

    if ENABLE_DOWNLOAD_MY_NOVEL:
        function_execute_time('download_my_novel', download_my_novel)

    function_execute_time('upload_to_drive all', upload_to_drive)

    def tmp_x() -> None:
        generate_drive_manga_exists(force_update=True)

    function_execute_time('generate_drive_manga_exists', tmp_x)

    function_execute_time('show_manga_updated', show_manga_updated)


if __name__ == "__main__":
    function_execute_time('execute download manga', run)
