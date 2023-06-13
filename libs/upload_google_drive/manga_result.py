import datetime
import json
import os
from collections import defaultdict

from ..utils.constants import MANGE_EXISTS_FILE_PATH

# sys.path.append("../../libs")  # Adds higher directory to python modules path.


def get_manga_updated(debug=False):
    if os.path.exists(MANGE_EXISTS_FILE_PATH):
        with open(MANGE_EXISTS_FILE_PATH, "r", encoding='utf-8') as read_file:
            manga_exists_json = json.load(read_file)

            results_yet_view = defaultdict(list)
            results_viewed = defaultdict(list)

            # manga_exists_json[project_dir['name']] = {
            #     "id": project_dir['id'],
            #     "sub_dirs": {}
            # }

            for project, mangaList in manga_exists_json.items():
                # print(f'project: {project}')

                for manga, manga_chanters in mangaList['sub_dirs'].items():
                    # print(f'manga: {manga}')
                    for chapter, chapter_detail in manga_chanters['chapters'].items():
                        modified_by_me_time = chapter_detail['modifiedByMeTime']
                        viewed_by_me = chapter_detail['viewedByMe']
                        modified_date_time = datetime.datetime.fromisoformat(modified_by_me_time)
                        modified_date = modified_date_time.strftime('%Y-%m-%d')
                        # print(f'chapter: {chapter}\tmodified_date: {modified_date}')

                        data = {
                            "project": project,
                            "manga": manga,
                            "chapter": chapter,
                            "viewedByMe": viewed_by_me
                        }

                        if viewed_by_me:
                            results_viewed[modified_date].append(data)
                        else:
                            results_yet_view[modified_date].append(data)

            results_yet_view_sorted = sorted(results_yet_view.items(), reverse=True)[:2:]
            results_viewed_sorted = sorted(results_viewed.items(), reverse=True)[:2:]

            if debug:
                print('\n--- VIEWED ---')
            for updated, item in results_viewed_sorted:
                if debug:
                    print(f'updated: {updated}')
                for e in list(sorted(set([f'{ d["project"]: <20} {d["manga"]}' for d in item]))):
                    # print('\tproject: {} {} {}'.format(e["project"], e["manga"], e["chapter"]))
                    if debug:
                        print(f'\t{e}')

            if debug:
                print('\n--- YET VIEW ---')
            for updated, item in results_yet_view_sorted:
                if debug:
                    print(f'updated: {updated}')
                for e in list(sorted(set([f'{d["project"]: <20} {d["manga"]} {d["chapter"]} {d["viewedByMe"]}' for d in item]))):
                    # print('\tproject: {} {} {}'.format(e["project"], e["manga"], e["chapter"]))
                    if debug:
                        print(f'\t{e}')
            return manga_exists_json, results_viewed_sorted, results_yet_view_sorted
