from typing import List


class ProjectCartoonItem:
    def __init__(self, title: str, image_pdf_list: List[str]):
        self.title = title
        self.image_pdf_list = image_pdf_list

class ProjectItem:
    def __init__(self, title: str,  sub_dirs: List[ProjectCartoonItem]):
        self.title = title
        self.sub_dirs = sub_dirs
        

