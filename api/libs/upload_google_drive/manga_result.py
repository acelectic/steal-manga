import datetime
import json
import os
from collections import defaultdict
from pprint import pprint

from ..utils.constants import MANGE_EXISTS_FILE_PATH
from ..utils.db_client import (
    StealMangaDb,
    get_count_manga_downloaded,
    get_manga_uploaded,
)
from ..utils.interface import MangaUploadedToDrive

# sys.path.append("../../libs")  # Adds higher directory to python modules path.


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


    def transform_data(data: list[MangaUploadedToDrive]):
        results = defaultdict(list)
        for d in data:
            modified_date_time = datetime.datetime.fromisoformat(d.modified_by_me_time)
            modified_date = modified_date_time.strftime('%Y-%m-%d')
            results[modified_date].append(d.to_json())
        return results

    # if os.path.exists(MANGE_EXISTS_FILE_PATH):
    #     with open(MANGE_EXISTS_FILE_PATH, "r", encoding='utf-8') as read_file:
    #         manga_exists_json = json.load(read_file)

    #         results_yet_view = defaultdict(list)
    #         results_viewed = defaultdict(list)

    #         # manga_exists_json[project_dir['name']] = {
    #         #     "id": project_dir['id'],
    #         #     "sub_dirs": {}
    #         # }

    #         for project, mangaList in manga_exists_json.items():
    #             # print(f'project: {project}')

    #             for manga, manga_chanters in mangaList['sub_dirs'].items():
    #                 # print(f'manga: {manga}')
    #                 for chapter, chapter_detail in manga_chanters['chapters'].items():
    #                     modified_by_me_time = chapter_detail['modifiedByMeTime']
    #                     viewed_by_me = chapter_detail['viewedByMe']
    #                     modified_date_time = datetime.datetime.fromisoformat(modified_by_me_time)
    #                     modified_date = modified_date_time.strftime('%Y-%m-%d')
    #                     # print(f'chapter: {chapter}\tmodified_date: {modified_date}')

    #                     data = {
    #                         "project": project,
    #                         "manga": manga,
    #                         "chapter": chapter,
    #                         "viewedByMe": viewed_by_me
    #                     }

    #                     if viewed_by_me:
    #                         results_viewed[modified_date].append(data)
    #                     else:
    #                         results_yet_view[modified_date].append(data)
    results_yet_view = transform_data(results_yet_view)
    results_viewed = transform_data(results_viewed)
    
    results_yet_view_sorted = sorted(results_yet_view.items(), reverse=True)[
        :latest_update:]
    results_viewed_sorted = sorted(results_viewed.items(), reverse=True)[:latest_update:]

    # if debug:
    #     print('\n--- VIEWED ---')
    # for updated, item in results_viewed_sorted:
    #     if debug:
    #         print(f'updated: {updated}')
    #     for e in list(sorted(set([f'{ d["project"]: <20} {d["manga"]}' for d in item]))):
    #         # print('\tproject: {} {} {}'.format(e["project"], e["manga"], e["chapter"]))
    #         if debug:
    #             print(f'\t{e}')

    # if debug:
    #     print('\n--- YET VIEW ---')
    # for updated, item in results_yet_view_sorted:
    #     if debug:
    #         print(f'updated: {updated}')
    #     for e in list(sorted(set([f'{d["project"]: <20} {d["manga"]} {d["chapter"]} {d["viewedByMe"]}' for d in item]))):
    #         # print('\tproject: {} {} {}'.format(e["project"], e["manga"], e["chapter"]))
    #         if debug:
    #             print(f'\t{e}')
                
    return results_viewed_sorted, results_yet_view_sorted, count_manga_downloaded_hash

