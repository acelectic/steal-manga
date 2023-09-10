from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .interface import UpdateMangaConfigData

from .constants import DB_PASSWORD, DB_USERNAME

uri: str = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@steal-manga.nlqv7lj.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
db_client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

try:
    db_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
def get_db():
    """ get db steal-manga """
    return db_client.get_database('steal-manga')

db = get_db()


def get_manga_config(project_name: str):
    """ get_manga_config """
    results = db.configs.find({
        "project_name": project_name
    })
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


