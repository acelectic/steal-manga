""" Main Module """
import sys
sys.path.append("../libs")

from libs.man_mirror import ManMirror
from libs.my_novel import MyNovel
from libs.upload_google_drive import generate_drive_manga_exists, upload_to_drive


def download_man_mirror():
    man_mirror_cartoons = [
        # ['เลเวลอัพไม่จำกัด', 1, 138, 141],
        # # ['สุดยอดจอมยุทธ', 7, 117, 118],
        # ['ดาบวายุอัสนี', 19, 64, 66],
        # ['จ้าวสงคราม', 3, 128, 130],
        # ['มือกระบี่ไร้พ่าย', 5, 150, 151],
        # # ['จิตวิญญาณวายุ', 16, 1, 76],
        # ['โกแซม นักรบในตำนาน', 12, 65, 66],
        # # ['บัณฑิตหวนคืน', 8, 1, 30],  # max 133
        ['เส้นทางสู่สวรรค์', 21, 1, 30],
        # # ['หนึ่งในใต้หล้า', 10, 1, 30],  # max 100
    ]
    for cartoon_name, cartoon_id, latest_chapter, max_chapter in man_mirror_cartoons:
        print(
            f'cartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}\tmax_chapter: {max_chapter}')
        man_mirror = ManMirror()
        man_mirror.download_cartoons(
            cartoon_name,
            cartoon_id, first_chapter=latest_chapter, max_chapter=max_chapter)

def download_my_novel():
    my_novel_cartoons = [
        # ['Against the Gods - อสูรพลิกฟ้า', '6EvFPzipwmnKxlZMqhjs', 423],
        ['Cultivator vs Superhero', '6yeQcr6kL14A96eUwKZA', 250],
        ['Tales of Demon and Gods', 'E8XDEk8Dv9vbchSGtF5n', 419],
        ['Infinite Mage','63b2a71156baafb4e8213126', 28]
    ]
    my_novel = MyNovel()
    for cartoon_name, cartoon_id, latest_chapter in my_novel_cartoons:
        print(
            f'cartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}')
        my_novel.download_cartoons(cartoon_id, start_ep_index=latest_chapter)


if __name__ == "__main__":
    ENABLE_DOWNLOAD_MAM_MIRROR = True
    ENABLE_DOWNLOAD_MY_NOVEL = False
    manga_exists_json = generate_drive_manga_exists()
    
    
    if ENABLE_DOWNLOAD_MAM_MIRROR:
        download_man_mirror()
    
    if ENABLE_DOWNLOAD_MY_NOVEL:
        download_my_novel()

    upload_to_drive()
    generate_drive_manga_exists(force_update=True)
    

    
