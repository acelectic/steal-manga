from pprint import pprint

from pymongo import ReturnDocument
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .constants import DB_PASSWORD, DB_USERNAME
from .interface import MangaUploadedToDrive, UpdateMangaConfigData

uri: str = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@steal-manga.nlqv7lj.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
db_client = MongoClient(uri, server_api=ServerApi('1'), connectTimeoutMS=60*1000, )
# Send a ping to confirm a successful connection

try:
    db_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

class StealMangaDb:
    """ StealMangaDb """
    
    db_name = 'steal-manga'
    table_name_config = 'configs'
    table_name_manga_upload = 'manga_uploads'
    
    
    
    def __init__(self) -> None:
        self.steal_manga_db = db_client.get_database(self.db_name)
        list_collection_names = self.steal_manga_db.list_collection_names()
        
        # create_collection if not exists
        if self.table_name_config not in list_collection_names:
            self.steal_manga_db.create_collection(self.table_name_config )
        
        if self.table_name_manga_upload not in list_collection_names:
            self.steal_manga_db.create_collection(self.table_name_manga_upload)
        
        # assign collection
        self.table_config = self.steal_manga_db[self.table_name_config]
        self.table_manga_upload = self.steal_manga_db[self.table_name_manga_upload]
        
        

def get_manga_config(project_name:str = ''):
    """ get_manga_config """
    where = None
    if(project_name != ''):
        where = {
            "project_name": project_name
        }
    steal_manga_db = StealMangaDb()
    results = steal_manga_db.table_config.find(where)
    data: list[UpdateMangaConfigData] = []
    for x in results:
        data.append(UpdateMangaConfigData(
            cartoon_name= x['cartoon_name'],
            cartoon_id= x['cartoon_id'],
            latest_chapter= x['latest_chapter'],
            max_chapter= x['max_chapter'],
            disabled= x['disabled'],
            downloaded= x['downloaded'],
            project_name= x['project_name'],
        ))
    return data 

def get_manga_uploaded(where=None):
    steal_manga_db = StealMangaDb()
    results = steal_manga_db.table_manga_upload.find(where)

    data: list[MangaUploadedToDrive] = []
    for x in results:
        data.append(MangaUploadedToDrive(
            project_name= x['project_name'],
            project_drive_id= x['project_drive_id'],
            cartoon_id= x['cartoon_id'],
            cartoon_name= x['cartoon_name'],
            cartoon_drive_id= x['cartoon_drive_id'],
            manga_chapter_name= x['manga_chapter_name'],
            manga_chapter_drive_id= x['manga_chapter_drive_id'],
            created_time= x['created_time'],
            modified_by_me_time= x['modified_by_me_time'],
            viewed_by_me= x['viewed_by_me'],
        ))
    return data


def get_count_manga_downloaded():
    steal_manga_db = StealMangaDb()
    count_manga_downloaded = steal_manga_db.table_manga_upload.aggregate([
        {"$group": {"_id": "$cartoon_id", "count": {"$sum": 1}}}
    ])
    count_manga_downloaded_hash:dict[str, int] = {}
    for d in count_manga_downloaded:
        count_manga_downloaded_hash[d['_id']] = d['count']
    return count_manga_downloaded_hash

def update_manga_downloaded():
    print('update_manga_downloaded')
    steal_manga_db = StealMangaDb()
    count_manga_downloaded = steal_manga_db.table_manga_upload.aggregate([
        {"$group": {"_id": "$cartoon_id", "count": {"$sum": 1}}}
    ])
    count_manga_downloaded2 = steal_manga_db.table_manga_upload.aggregate([
        {"$group": {"_id": "$cartoon_name", "count": {"$sum": 1}}}
    ])

    pprint(list(count_manga_downloaded2))
    print(f'update_manga_downloaded: {len(list(count_manga_downloaded))}')

    for d in count_manga_downloaded:
        cartoon_id = d['_id']
        downloaded = d['count']
        result_downloaded = steal_manga_db.table_config.find_one_and_update(
            filter={
                "cartoon_id": cartoon_id,
            },
            update={
                '$set': {
                    "downloaded": downloaded
                }
            },
            upsert=False,
            return_document = ReturnDocument.AFTER
        )
        pprint(result_downloaded)
    print('update_manga_downloaded end')

