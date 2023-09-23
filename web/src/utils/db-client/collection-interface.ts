import { Document } from 'mongodb'

export interface IMangaWebData extends Document {
  id: string
  name: string
  link: string
}

export interface IUpdateMangaWebPayload {
  mangaWebs: IMangaWebData[]
}
