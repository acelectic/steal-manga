""" interface module """


class UpdateMangaConfigData:
    """ UpdateMangaConfigData """
    cartoon_name: str
    cartoon_id: str
    latest_chapter: int
    max_chapter: int
    disabled: bool
    downloaded: int
    project_name: str

    def __init__(self,
                 cartoon_name: str,
                 cartoon_id: str,
                 latest_chapter: int,
                 max_chapter: int,
                 disabled: bool,
                 downloaded: int,
                 project_name: str) -> None:
        self.cartoon_name = cartoon_name
        self.cartoon_id = cartoon_id
        self.latest_chapter = latest_chapter
        self.max_chapter = max_chapter
        self.disabled = disabled
        self.downloaded = downloaded
        self.project_name = project_name
        
    def to_json(self):
        """ to json """
        return {
            "cartoon_name": self.cartoon_name,
            "cartoon_id": self.cartoon_id,
            "latest_chapter": self.latest_chapter,
            "max_chapter": self.max_chapter,
            "disabled": self.disabled,
            "downloaded": self.downloaded,
            "project_name": self.project_name,
        }
