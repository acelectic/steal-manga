""" interface module """


class UpdateMangaConfigData:
    """ UpdateMangaConfigData """

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

    def __init__(self,
                 project_name: str = '',
                 project_drive_id: str = '',
                 cartoon_id: str = '',
                 cartoon_name: str = '',
                 cartoon_drive_id: str = '',
                 manga_chapter_name: str = '',
                 manga_chapter_drive_id: str = '',
                 created_time: str = '',
                 modified_by_me_time: str = '',
                 viewed_by_me: bool = False,
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

    def to_where(self):
        where = {}
        if self.project_name != '' and self.project_name is not None:
            where["project_name"] = self.project_name
        if self.project_drive_id != '' and self.project_drive_id is not None:
            where["project_drive_id"] = self.project_drive_id
        if self.cartoon_id != '' and self.cartoon_id is not None:
            where["cartoon_id"] = self.cartoon_id
        if self.cartoon_name != '' and self.cartoon_name is not None:
            where["cartoon_name"] = self.cartoon_name
        if self.cartoon_drive_id != '' and self.cartoon_drive_id is not None:
            where["cartoon_drive_id"] = self.cartoon_drive_id
        if self.manga_chapter_name != '' and self.manga_chapter_name is not None:
            where["manga_chapter_name"] = self.manga_chapter_name
        if self.manga_chapter_drive_id != '' and self.manga_chapter_drive_id is not None:
            where["manga_chapter_drive_id"] = self.manga_chapter_drive_id
        if self.created_time != '' and self.created_time is not None:
            where["created_time"] = self.created_time
        if self.modified_by_me_time != '' and self.modified_by_me_time is not None:
            where["modified_by_me_time"] = self.modified_by_me_time
        return where
