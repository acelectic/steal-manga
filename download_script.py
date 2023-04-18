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

def download_man_mirror_manual():
    cartoons = [
     {
    "cartoon_name": "เทพมรณะ",
    "cartoon_id": 22,
    "chapters": [
        {
            "chapter_name": "0",
            "image_paths": [
                "https://www.manmirror.net/test/22/0/DG00-1_001.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_002.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_003.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_004.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_005.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_006.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_007.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_008.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_009.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_010.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_011.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_012.jpg",
                "https://www.manmirror.net/test/22/0/DG00-1_013.jpg",
                "https://www.manmirror.net/test/22/0/DG00-2_001.jpg",
                "https://www.manmirror.net/test/22/0/DG00-2_002.jpg",
                "https://www.manmirror.net/test/22/0/DG00-2_003.jpg",
                "https://www.manmirror.net/test/22/0/DG00-2_004.jpg",
                "https://www.manmirror.net/test/22/0/DG00-2_005.jpg",
                "https://www.manmirror.net/test/22/0/DG00-2_006.jpg",
                "https://www.manmirror.net/test/22/0/DG00-2_007.jpg",
                "https://www.manmirror.net/test/22/0/DG00-2_008.jpg",
                "https://www.manmirror.net/test/22/0/DG00-2_009.jpg",
                "https://www.manmirror.net/test/22/0/DG00-2_010.jpg",
                "https://www.manmirror.net/test/22/0/DG00-2_011.jpg",
                "https://www.manmirror.net/test/22/0/DG00-3_001.jpg",
                "https://www.manmirror.net/test/22/0/DG00-3_002.jpg",
                "https://www.manmirror.net/test/22/0/DG00-3_003.jpg",
                "https://www.manmirror.net/test/22/0/DG00-3_004.jpg",
                "https://www.manmirror.net/test/22/0/DG00-3_005.jpg",
                "https://www.manmirror.net/test/22/0/DG00-3_006.jpg",
                "https://www.manmirror.net/test/22/0/DG00-3_007.jpg",
                "https://www.manmirror.net/test/22/0/DG00-3_008.jpg",
                "https://www.manmirror.net/test/22/0/DG00-3_009.jpg",
                "https://www.manmirror.net/test/22/0/DG00-3_010.jpg",
                "https://www.manmirror.net/test/22/0/DG00-3_011.jpg"
            ]
        },
        {
            "chapter_name": "1",
            "image_paths": [
                "https://www.manmirror.net/test/22/1/DG01-1_001.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_002.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_003.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_004.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_005.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_006.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_007.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_008.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_009.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_010.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_011.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_012.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_013.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_014.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_015.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_016.jpg",
                "https://www.manmirror.net/test/22/1/DG01-1_017.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_001.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_002.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_003.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_004.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_005.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_006.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_007.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_008.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_009.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_010.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_011.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_012.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_013.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_014.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_015.jpg",
                "https://www.manmirror.net/test/22/1/DG01-2_016.jpg"
            ]
        },
        {
            "chapter_name": "2",
            "image_paths": [
                "https://www.manmirror.net/test/22/2/DG02-1_001.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_002.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_003.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_004.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_005.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_006.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_007.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_008.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_009.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_010.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_011.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_012.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_013.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_014.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_015.jpg",
                "https://www.manmirror.net/test/22/2/DG02-1_016.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_001.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_002.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_003.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_004.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_005.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_006.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_007.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_008.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_009.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_010.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_011.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_012.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_013.jpg",
                "https://www.manmirror.net/test/22/2/DG02-2_014.jpg"
            ]
        },
        {
            "chapter_name": "3",
            "image_paths": [
                "https://www.manmirror.net/test/22/3/DG03-1_001.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_002.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_003.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_004.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_005.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_006.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_007.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_008.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_009.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_010.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_011.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_012.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_013.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_014.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_015.jpg",
                "https://www.manmirror.net/test/22/3/DG03-1_016.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_001.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_002.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_003.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_004.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_005.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_006.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_007.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_008.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_009.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_010.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_011.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_012.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_013.jpg",
                "https://www.manmirror.net/test/22/3/DG03-2_014.jpg"
            ]
        },
        {
            "chapter_name": "4",
            "image_paths": [
                "https://www.manmirror.net/test/22/4/DG04-1_001.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_002.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_003.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_004.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_005.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_006.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_007.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_008.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_009.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_010.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_011.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_012.jpg",
                "https://www.manmirror.net/test/22/4/DG04-1_013.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_001.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_002.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_003.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_004.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_005.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_006.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_007.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_008.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_009.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_010.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_011.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_012.jpg",
                "https://www.manmirror.net/test/22/4/DG04-2_013.jpg"
            ]
        },
        {
            "chapter_name": "5",
            "image_paths": [
                "https://www.manmirror.net/test/22/5/DG05-1_001.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_002.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_003.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_004.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_005.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_006.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_007.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_008.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_009.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_010.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_011.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_012.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_013.jpg",
                "https://www.manmirror.net/test/22/5/DG05-1_014.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_001.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_002.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_003.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_004.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_005.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_006.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_007.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_008.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_009.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_010.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_011.jpg",
                "https://www.manmirror.net/test/22/5/DG05-2_012.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_001.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_002.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_003.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_004.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_005.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_006.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_007.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_008.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_009.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_010.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_011.jpg",
                "https://www.manmirror.net/test/22/5/DG05-3_012.jpg"
            ]
        },
    ]
}
    ]
    
    man_mirror = ManMirror()
    
    for cartoon in cartoons:
        cartoon_name = cartoon["cartoon_name"]
        cartoon_id = cartoon["cartoon_id"]
        
        for chapter in cartoon['chapters']:
            chapter_name = chapter["chapter_name"]
            image_paths = chapter["image_paths"]
            man_mirror.download_manual( cartoon_id=cartoon_id,  cartoon_name=cartoon_name, chapter = chapter_name, image_paths=image_paths )
        

def download_man_mirror():
    man_mirror_cartoons = [
        ['เลเวลอัพไม่จำกัด', 1, 138, 144],
        ['สุดยอดจอมยุทธ', 7, 1, 118],
        ['ดาบวายุอัสนี', 19, 1, 70],
        ['จ้าวสงคราม', 3, 65, 132],
        ['มือกระบี่ไร้พ่าย', 5, 1, 156],
        # ['จิตวิญญาณวายุ', 16, 1, 76],
        # ['โกแซม นักรบในตำนาน', 12, 65, 66],
        # ['บัณฑิตหวนคืน', 8, 1, 133],  # max 133
        ['เส้นทางสู่สวรรค์', 21, 35, 53],
        ['มังกรพิษ', 6, 1, 128],
        # ['หนึ่งในใต้หล้า', 10, 1, 111],  # max 100
        ['ตำนานกระบี่อุดร', 9, 150, 151],
        ['เทพมรณะ', 22, 1, 36],
        # ['เทพอัสนี', 11, 1, 141],
        ['ทายาทจอมมาร', 2, 1, 80],
        ['ทายาทเทพธนู', 20, 1, 50]
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
    ENABLE_DOWNLOAD_MAM_MIRROR_MANUAL = True
    ENABLE_DOWNLOAD_MY_NOVEL = True
    # manga_exists_json = generate_drive_manga_exists(force_update=True, logging=False)


    if ENABLE_DOWNLOAD_MAM_MIRROR:
        download_man_mirror()

    if ENABLE_DOWNLOAD_MY_NOVEL:
        download_my_novel()
        
    if ENABLE_DOWNLOAD_MAM_MIRROR_MANUAL:
        download_man_mirror_manual()


    upload_to_drive(logging=True)
    generate_drive_manga_exists(force_update=True)
    show_manga_updated()
