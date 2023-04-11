""" Main Module """
import sys


sys.path.append("./libs")
sys.path.append("./libs/upload_google_drive")

from libs.man_mirror import ManMirror
from libs.my_novel import MyNovel
from libs.upload_google_drive import generate_drive_manga_exists, upload_to_drive
from libs.upload_google_drive.manga_result import show_manga_updated
from dotenv import load_dotenv

load_dotenv()

MAX_WORKERS = 10

def download_man_mirror():
    man_mirror_cartoons = [
        ['เลเวลอัพไม่จำกัด', 1, 138, 143],
        ['สุดยอดจอมยุทธ', 7, 1, 118],
        ['ดาบวายุอัสนี', 19, 1, 68],
        # ['จ้าวสงคราม', 3, 65, 130],
        ['มือกระบี่ไร้พ่าย', 5, 1, 155],
        # ['จิตวิญญาณวายุ', 16, 1, 76],
        # ['โกแซม นักรบในตำนาน', 12, 65, 66],
        # ['บัณฑิตหวนคืน', 8, 1, 133],  # max 133
        ['เส้นทางสู่สวรรค์', 21, 35, 48],
        ['มังกรพิษ', 6, 1, 127],
        # ['หนึ่งในใต้หล้า', 10, 1, 111],  # max 100
        ['ตำนานกระบี่อุดร', 9, 150, 151],
        # ['เทพมรณะ', 22, 1, 31],
        # ['เทพอัสนี', 11, 1, 141],
        ['ทายาทจอมมาร', 2, 1, 75],
        ['ทายาทเทพธนู', 20, 1, 46]
    ]

    for cartoon_name, cartoon_id, latest_chapter, max_chapter in man_mirror_cartoons:
        print(
            f'cartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}\tmax_chapter: {max_chapter}')
        manga_exists_json = generate_drive_manga_exists(force_update=True)
        man_mirror = ManMirror()
        man_mirror.download_cartoons(
            cartoon_name,
            cartoon_id, first_chapter=latest_chapter, max_chapter=max_chapter, manga_exists_json=manga_exists_json, max_workers=MAX_WORKERS)
        after_each_manga_downloaded()

def download_my_novel():
    my_novel_cartoons = [
        # ['Against the Gods - อสูรพลิกฟ้า', '6EvFPzipwmnKxlZMqhjs', 423],
        ['Cultivator vs Superhero', '6yeQcr6kL14A96eUwKZA', 250],
        ['Tales of Demon and Gods', 'E8XDEk8Dv9vbchSGtF5n', 419],
        ['Infinite Mage','63b2a71156baafb4e8213126', 1]
    ]
    my_novel = MyNovel()
    for cartoon_name, cartoon_id, latest_chapter in my_novel_cartoons:
        manga_exists_json = generate_drive_manga_exists(force_update=True)
        print(
            f'cartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}')
        my_novel.download_cartoons(cartoon_id, start_ep_index=latest_chapter, manga_exists_json=manga_exists_json,max_workers=MAX_WORKERS)
        after_each_manga_downloaded()
        
def after_each_manga_downloaded():
    upload_to_drive()
    # manga_exists_json = generate_drive_manga_exists(force_update=True)
    # return manga_exists_json

if __name__ == "__main__":
    ENABLE_DOWNLOAD_MAM_MIRROR = True
    ENABLE_DOWNLOAD_MY_NOVEL = True
    # manga_exists_json = generate_drive_manga_exists(force_update=True, logging=False)


    if ENABLE_DOWNLOAD_MAM_MIRROR:
        download_man_mirror()

    if ENABLE_DOWNLOAD_MY_NOVEL:
        download_my_novel()


    # upload_to_drive(logging=True)
    # generate_drive_manga_exists(force_update=True)
    show_manga_updated()
