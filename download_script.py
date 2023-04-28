""" Main Module """
from time import time

from dotenv import load_dotenv

from libs.man_mirror import ManMirror
from libs.my_novel import MyNovel
from libs.upload_google_drive import generate_drive_manga_exists, upload_to_drive
from libs.upload_google_drive.manga_result import show_manga_updated

# sys.path.append("./libs")
# sys.path.append("./libs/upload_google_drive")


load_dotenv()

MAX_WORKERS = 1


def download_man_mirror_manual() -> None:
    cartoons = [
        {
            "cartoon_name": "เทพมรณะ",
            "cartoon_id": 22,
            "chapters": [
                {
                    "chapter_name": "0",
                },
                {
                    "chapter_name": "1",
                },
                {
                    "chapter_name": "2",
                },
                {
                    "chapter_name": "3",
                },
                {
                    "chapter_name": "4",
                },
                {
                    "chapter_name": "5",
                },
            ]
        }
    ]

    man_mirror = ManMirror()

    for cartoon in cartoons:
        cartoon_name = cartoon["cartoon_name"]
        cartoon_id = cartoon["cartoon_id"]
        manga_exists_json = generate_drive_manga_exists(force_update=True)

        for chapter in cartoon['chapters']:
            chapter_name = chapter["chapter_name"]
            # image_paths = chapter["image_paths"]
            man_mirror.download_manual(cartoon_id=cartoon_id,  cartoon_name=cartoon_name,
                                       chapter=chapter_name, manga_exists_json=manga_exists_json)


def download_man_mirror():
    man_mirror_cartoons = [
        ['เลเวลอัพไม่จำกัด', 1, 138, 145],
        ['สุดยอดจอมยุทธ', 7, 1, 118],
        ['ดาบวายุอัสนี', 19, 21, 70],
        ['จ้าวสงคราม', 3, 65, 133],
        ['มือกระบี่ไร้พ่าย', 5, 100, 158],
        # ['จิตวิญญาณวายุ', 16, 1, 76],
        # ['โกแซม นักรบในตำนาน', 12, 65, 66],
        # ['บัณฑิตหวนคืน', 8, 1, 133],  # max 133
        ['เส้นทางสู่สวรรค์', 21, 35, 62],
        ['มังกรพิษ', 6, 120, 130],
        # ['หนึ่งในใต้หล้า', 10, 1, 111],  # max 100
        ['ตำนานกระบี่อุดร', 9, 150, 153],
        ['เทพมรณะ', 22, 1, 36],
        # ['เทพอัสนี', 11, 1, 141],
        ['ทายาทจอมมาร', 2, 1, 81],
        ['ทายาทเทพธนู', 20, 1, 50]
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
