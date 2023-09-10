from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .interface import UpdateMangaConfigData

from .constants import DB_PASSWORD, DB_USERNAME

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


