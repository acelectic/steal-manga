
from pymongo import ReturnDocument

from ..utils.db_client import StealMangaDb
from ..utils.interface import UpdateMangaConfigData


def update_manga_config(data: UpdateMangaConfigData):
    """ update_manga_config """
    success = False
    steal_manga_db = StealMangaDb()
    steal_manga_db.table_manga_config.find()

    try:
        steal_manga_db.table_manga_config.find_one_and_update(
            filter={
                "cartoon_id": data.cartoon_id,
            },
            update={
                '$set': data.to_json()
            },
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        success = True
    except Exception as e:
        print(e)
        raise e

    return success
