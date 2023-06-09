import json
import os

from ..utils.constants import MANGE_ROOT_DIR
from ..utils.interface import UpdateMangaConfigData


def update_manga_config(data: UpdateMangaConfigData):
    success = False
    if data.project_name == 'man-mirror':
        man_mirror_cartoons = []
        with open(os.path.join(MANGE_ROOT_DIR,  'man-mirror.json'), 'r', encoding='utf-8') as f:
            man_mirror_cartoons = json.load(f)

        for i, d in enumerate(man_mirror_cartoons):
            cartoon_name, cartoon_id, latest_chapter, max_chapter, disabled = d
            if cartoon_id == data.cartoon_id:
                man_mirror_cartoons[i] = [cartoon_name, cartoon_id,
                                          int(data.latest_chapter), int(data.max_chapter), data.disabled]

        with open(os.path.join(MANGE_ROOT_DIR,  'man-mirror.json'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(man_mirror_cartoons, indent=4, ensure_ascii=False))

        success = True

    if data.project_name == 'my-novel':
        my_novel_cartoons = []
        with open(os.path.join(MANGE_ROOT_DIR,  'my-novel.json'), 'r', encoding='utf-8') as f:
            my_novel_cartoons = json.load(f)

        for i, d in enumerate(my_novel_cartoons):
            cartoon_name, cartoon_id, latest_chapter, disabled = d
            if cartoon_id == data.cartoon_id:
                my_novel_cartoons[i] = [cartoon_name, cartoon_id,
                                        int(data.latest_chapter),  data.disabled]

        with open(os.path.join(MANGE_ROOT_DIR,  'my-novel.json'), 'w', encoding='utf-8') as f:
            f.write(json.dumps(my_novel_cartoons, indent=4, ensure_ascii=False))
        success = True
    return success
