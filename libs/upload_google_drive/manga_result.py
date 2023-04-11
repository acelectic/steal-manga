from collections import defaultdict
import datetime
import json
import os
import sys

from libs.utils.constants import MANGE_EXISTS_FILE_PATH

sys.path.append("../../libs")  # Adds higher directory to python modules path.


def show_manga_updated():
    if os.path.exists(MANGE_EXISTS_FILE_PATH):
            with open(MANGE_EXISTS_FILE_PATH, "r", encoding='utf-8') as read_file:
                manga_exists_json = json.load(read_file)
                
                
                results = defaultdict(list)
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
                            modified_date_time = datetime.datetime.fromisoformat(modified_by_me_time)
                            modified_date = modified_date_time.strftime('%Y-%m-%d')
                            # print(f'chapter: {chapter}\tmodified_date: {modified_date}')
                                
                            results[modified_date].append({
                                "project": project,
                                "manga": manga,
                                "chapter": chapter,
                            })
                for updated, item in sorted(results.items(),reverse=True)[:1:]:
                    print(f'updated: {updated}')
                    for e in item:
                        print('\tproject: {} {} {}'.format(e["project"], e["manga"], e["chapter"]))
                # drive_project_manga_dirs = list_drive_dirs(
                #     service, project_dir['id'])
                # for manga_dir in drive_project_manga_dirs[::]:
                #     if logging:
                #         print(u'\t{0} ({1})'.format(
                #         manga_dir['name'], manga_dir['id']))

                #     manga_exists_json[project_dir['name']]["sub_dirs"][manga_dir['name']] = {
                #         "id": manga_dir['id'],
                #         "chapters": {}
                #     }

                #     drive_manga_chapters = list_drive_manga(
                #         service, manga_dir['id'])
                #     for drive_manga_chapter in drive_manga_chapters[::]:
                #         if logging:
                #             print(u'\t\t{0} ({1})'.format(
                #             drive_manga_chapter['name'], drive_manga_chapter['id']))
                #         manga_exists_json[project_dir['name']]["sub_dirs"][manga_dir['name']]["chapters"][drive_manga_chapter['name']] = {
                #         "id": drive_manga_chapter['id'],
                #         "createdTime": drive_manga_chapter['createdTime'], 
                #         "modifiedByMeTime": drive_manga_chapter['modifiedByMeTime']
                #     }
                
                
