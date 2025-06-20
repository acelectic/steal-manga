
from pymongo import ReturnDocument
import logging
from ..utils.logging_helper import setup_logging

from ..upload_google_drive import update_latest_sync
from ..utils.db_client import StealMangaDb
from ..utils.interface import UpdateMangaConfigData

setup_logging()
logger = logging.getLogger(__name__)


def update_manga_config(data: UpdateMangaConfigData):
    """ update_manga_config """
    success = False
    steal_manga_db = StealMangaDb()

    try:
        update_latest_sync(data.cartoon_id)

        steal_manga_db.table_manga_config.find_one_and_update(
            filter={
                "cartoon_id": data.cartoon_id,
            },
            update={
                '$set': data.to_json()  # type: ignore
            },
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        success = True
    except Exception as e:
        logger.error(e)
        raise e

    return success
