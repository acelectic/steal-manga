
from pymongo import ReturnDocument

from ..utils.interface import UpdateMangaConfigData
from ..utils.db_client import StealMangaDb


def update_manga_config(data: UpdateMangaConfigData):
    """ update_manga_config """
    success = False
    steal_manga_db = StealMangaDb()
    
    try:
        steal_manga_db.table_config.find_one_and_update(
            filter={
                "cartoon_id": data.cartoon_id,
            },
            update={
                '$set': data.to_json()    
            },
            upsert=False,
            return_document = ReturnDocument.AFTER
        )
        success = True
    except Exception as e:
        print(e)
        raise e
    
    # if data.project_name == 'man-mirror':
    #     man_mirror_cartoons = []
    #     with open(os.path.join(MANGE_ROOT_DIR,  'man-mirror.json'), 'r', encoding='utf-8') as f:
    #         man_mirror_cartoons = json.load(f)

    #     for i, d in enumerate(man_mirror_cartoons):
    #         cartoon_name, cartoon_id, latest_chapter, max_chapter, disabled = d
    #         if cartoon_id == data.cartoon_id:
    #             man_mirror_cartoons[i] = [cartoon_name, cartoon_id,
    #                                       int(data.latest_chapter), int(data.max_chapter), data.disabled]

    #     with open(os.path.join(MANGE_ROOT_DIR,  'man-mirror.json'), 'w', encoding='utf-8') as f:
    #         f.write(json.dumps(man_mirror_cartoons, indent=2, ensure_ascii=False))

    #     success = True

    # if data.project_name == 'my-novel':
    #     my_novel_cartoons = []
    #     with open(os.path.join(MANGE_ROOT_DIR,  'my-novel.json'), 'r', encoding='utf-8') as f:
    #         my_novel_cartoons = json.load(f)

    #     for i, d in enumerate(my_novel_cartoons):
    #         cartoon_name, cartoon_id, latest_chapter, disabled = d
    #         if cartoon_id == data.cartoon_id:
    #             my_novel_cartoons[i] = [cartoon_name, cartoon_id,
    #                                     int(data.latest_chapter),  data.disabled]

    #     with open(os.path.join(MANGE_ROOT_DIR,  'my-novel.json'), 'w', encoding='utf-8') as f:
    #         f.write(json.dumps(my_novel_cartoons, indent=2, ensure_ascii=False,
    #                 sort_keys=True, separators=(',', ': ')))
    #     success = True
    return success
