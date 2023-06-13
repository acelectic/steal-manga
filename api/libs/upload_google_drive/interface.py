from typing import List


class ProjectCartoonItem:
    """ ProjectCartoonItem """

    def __init__(self, title: str, image_pdf_list: List[str]) -> None:
        self.title: str = title
        self.image_pdf_list: List[str] = image_pdf_list


class ProjectItem:
    """ ProjectItem """

    def __init__(self, title: str,  sub_dirs: List[ProjectCartoonItem]) -> None:
        self.title: str = title
        self.sub_dirs: List[ProjectCartoonItem] = sub_dirs


class ManualManMirrorMangaItem:
    """ ManualManMirrorMangaItem """

    def __init__(self, cartoon_name: str, cartoon_id: str, prefix: str, active: bool, chapters: List[str]) -> None:
        self.cartoon_name: str = cartoon_name
        self.cartoon_id: str = cartoon_id
        self.prefix: str = prefix
        self.active: bool = active
        self.chapters: List[str] = chapters
