""" Main Module """
from time import time
from typing import List

from dotenv import load_dotenv

from libs.man_mirror import ManMirror
from libs.my_novel import MyNovel
from libs.upload_google_drive import generate_drive_manga_exists, upload_to_drive
from libs.upload_google_drive.interface import ManualManMirrorMangaItem
from libs.upload_google_drive.manga_result import get_manga_updated

load_dotenv()

MAX_WORKERS = 4


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
        ['เลเวลอัพไม่จำกัด', 1, 138, 151],
        ['สุดยอดจอมยุทธ', 7, 1, 118],
        ['ดาบวายุอัสนี', 19, 21, 75],
        ['จ้าวสงคราม', 3, 65, 135],
        ['มือกระบี่ไร้พ่าย', 5, 100, 164],
        # ['จิตวิญญาณวายุ', 16, 1, 76],
        # ['โกแซม นักรบในตำนาน', 12, 65, 66],
        ['บัณฑิตหวนคืน', 8, 1, 152],  # max 133
        ['เส้นทางสู่สวรรค์', 21, 35, 80],
        ['มังกรพิษ', 6, 120, 133],
        # ['หนึ่งในใต้หล้า', 10, 1, 111],  # max 100
        ['ตำนานกระบี่อุดร', 9, 150, 159],
        ['เทพมรณะ', 22, 1, 41],
        # ['เทพอัสนี', 11, 1, 141],
        ['ทายาทจอมมาร', 2, 1, 86],
        ['ทายาทเทพธนู', 20, 1, 57],
        ['ขุนศึก', 24, 30, 69],
        ['เมื่อผมดันหยิบมือถือจากโลกอื่น', 23, 1, 60],
        ['โคตรสำนักพิทักษ์ยุทธจักร', 25, 1, 2]
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
        ['Infinite Mage', '63b2a71156baafb4e8213126', 36],
        ['ทรินิตี้ วอนเดอร์ (จบ)', '8Kb8DMuuruSwn01xezjZ', 1],
        ["เลเวียธาน อสูรกายใต้สมุทร (จบ)", '9HqI9mCFDjaWNgV1tPVe', 1],
        ['Memorize', 'J3nr2EfolkNXsNMfRvrL', 1],
        ["The doctor's Supremacy", 'rkWEPd7GY52WCBvYnnzd', 1],
        ["Song of Taoists and Fairies", 'tYvMf0dvUAwcyR9RngTm', 1],
        ["โกซู แค้นทลายฟ้า ซีซั่น 2 (อวสาน)", '62218d8d5a6d7edb4e933ec4', 1],
        ["ตูข้านี่แหละเทพ (ทันจีน)", "BFQhu3i0uzJPV9J3xD3G", 1],
        ["The Lazy Prince Becomes a Genius", "OQkzfkZfGLyILTMDBVKG", 1],
        ["Red Storm - พายุสีเลือด", "6261162334a41e43920fb45a", 1]
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

    function_execute_time('upload_to_drive all', upload_to_drive)

    function_execute_time('generate_drive_manga_exists', tmp_x)

    function_execute_time('show_manga_updated', get_manga_updated, debug=debug)


if __name__ == "__main__":
    function_execute_time('execute download manga', execute_download,
                          enable_download_mam_mirror=True,
                          enable_download_mam_mirror_manual=False,
                          enable_download_my_novel=True,
                          debug=True,
                          )
