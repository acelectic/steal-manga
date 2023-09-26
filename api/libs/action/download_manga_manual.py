
from ..man_mirror import ManMirror
from ..my_novel import MyNovel
from ..upload_google_drive import generate_drive_manga_exists, upload_to_drive
from ..utils.interface import UpdateMangaConfigData


def download_manga_manual(data: UpdateMangaConfigData, auto_update_config: bool = True):
    success = False
    cartoon_name = data.cartoon_name
    cartoon_id = data.cartoon_id
    latest_chapter = data.latest_chapter
    max_chapter = data.max_chapter

    if data.project_name == 'man-mirror':
        man_mirror = ManMirror()
        generate_drive_manga_exists(target_project_name=man_mirror.project_name)

        print(
            f'\ncartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}\tmax_chapter: {max_chapter}')
        man_mirror.download_cartoons(
            cartoon_name,
            cartoon_id,
            first_chapter=latest_chapter,
            max_chapter=max_chapter,
            max_workers=1
        )
        upload_to_drive(
            project_name=man_mirror.project_name)

        if auto_update_config:
            generate_drive_manga_exists(target_project_name=man_mirror.project_name)

        success = True

    if data.project_name == 'my-novel':
        my_novel = MyNovel()
        generate_drive_manga_exists(target_project_name=my_novel.project_name)
        print(
            f'\ncartoon_name: {cartoon_name}\tkey: {cartoon_id}\tlatest_chapter: {latest_chapter}')
        my_novel.download_cartoons(str(cartoon_id), cartoon_name=cartoon_name,
                                   start_ep_index=latest_chapter, max_workers=1)
        upload_to_drive(project_name=my_novel.project_name)

        if auto_update_config:
            generate_drive_manga_exists(target_project_name=my_novel.project_name)

        success = True
    return success
