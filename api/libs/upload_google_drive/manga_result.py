import datetime
from collections import defaultdict
import logging
from ..utils.logging_helper import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

from ..utils.db_client import get_count_manga_downloaded, get_manga_uploaded
from ..utils.interface import MangaUploadedToDrive


def get_manga_updated(latest_update=None, debug=False):
    if latest_update is None:
        latest_update = 2
    else:
        latest_update = int(latest_update)

    results_yet_view = get_manga_uploaded({
        "viewed_by_me": False
    })
    results_viewed = get_manga_uploaded({
        "viewed_by_me": True
    })
    count_manga_downloaded_hash = get_count_manga_downloaded()
    if debug:
        logger.debug(count_manga_downloaded_hash)

    def transform_data(data: list[MangaUploadedToDrive]):
        results = defaultdict(list)
        for d in data:
            modified_date_time = datetime.datetime.fromisoformat(d.modified_by_me_time)
            modified_date = modified_date_time.strftime('%Y-%m-%d')
            results[modified_date].append(d.to_json())
        return results

    results_yet_view = transform_data(results_yet_view)
    results_viewed = transform_data(results_viewed)

    results_yet_view_sorted = sorted(results_yet_view.items(), reverse=True)[
        :latest_update:]
    results_viewed_sorted = sorted(results_viewed.items(), reverse=True)[:latest_update:]

    return results_viewed_sorted, results_yet_view_sorted
