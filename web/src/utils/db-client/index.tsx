import {
  AnyBulkWriteOperation,
  Collection,
  Db,
  Filter,
  MongoClient,
  ServerApiVersion,
} from 'mongodb'
import { appConfig } from '../../config/app-config'
import { IMangaUpload, IMangaWebData } from './collection-interface'

export class DbClient {
  private _uri: string
  private client: MongoClient
  private db: Db
  table_manga_web: Collection<IMangaWebData>
  table_manga_upload: Collection<IMangaUpload>

  constructor(dbUsername: string, dbPassword: string) {
    this._uri = `mongodb+srv://${dbUsername}:${dbPassword}@${appConfig.DB_NAME}.nlqv7lj.mongodb.net/?retryWrites=true&w=majority`
    const client = new MongoClient(this._uri, {
      serverApi: {
        version: ServerApiVersion.v1,
        strict: true,
        deprecationErrors: true,
      },
    })
    client.connect()
    // Create a MongoClient with a MongoClientOptions object to set the Stable API version
    this.client = client
    this.db = client.db(appConfig.DB_NAME)
    this.table_manga_web = this.db.collection<IMangaWebData>('manga_webs')
    this.table_manga_upload = this.db.collection<IMangaUpload>('manga_uploads')
  }

  static get init() {
    return new DbClient(appConfig.DB_USERNAME, appConfig.DB_PASSWORD)
  }

  updateBookmarkMangaWeb(mangaWebs: IMangaWebData[]) {
    const requests = mangaWebs.map((mangaWeb): AnyBulkWriteOperation<IMangaWebData> => {
      const filter: Filter<IMangaWebData> = {}
      if (mangaWeb.id) {
        filter.id = mangaWeb.id
      } else {
        filter.name = mangaWeb.name
      }

      return {
        replaceOne: {
          filter: filter,
          replacement: mangaWeb,
          upsert: true,
        },
      }
    })
    return this.table_manga_web.bulkWrite(requests)
  }
}
