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


class MangaUploadedToDrive:
    """ UpdateMangaConfigData """
    project_name: str
    project_drive_id: str
    cartoon_id: str
    cartoon_name: str
    cartoon_drive_id: str
    manga_chapter_name: str
    manga_chapter_drive_id: str
    
    created_time: str
    modified_by_me_time: str
    viewed_by_me: str

    def __init__(self,
                project_name: str,
                project_drive_id: str,
                cartoon_id: str,
                cartoon_name: str,
                cartoon_drive_id: str,
                manga_chapter_name: str,
                manga_chapter_drive_id: str,
                created_time: str,
                modified_by_me_time: str,
                viewed_by_me: str,
) -> None:
        self.project_name = project_name
        self.project_drive_id = project_drive_id
        self.cartoon_id = cartoon_id
        self.cartoon_name = cartoon_name
        self.cartoon_drive_id = cartoon_drive_id
        self.manga_chapter_name = manga_chapter_name
        self.manga_chapter_drive_id = manga_chapter_drive_id
        self.created_time = created_time
        self.modified_by_me_time = modified_by_me_time
        self.viewed_by_me = viewed_by_me
        
    def to_json(self):
        """ to json """
        return {
            "project_name": self.project_name,
            "project_drive_id": self.project_drive_id,
            "cartoon_id": self.cartoon_id,
            "cartoon_name": self.cartoon_name,
            "cartoon_drive_id": self.cartoon_drive_id,
            "manga_chapter_name": self.manga_chapter_name,
            "manga_chapter_drive_id": self.manga_chapter_drive_id,
            "created_time": self.created_time,
            "modified_by_me_time": self.modified_by_me_time,
            "viewed_by_me": self.viewed_by_me,
        }