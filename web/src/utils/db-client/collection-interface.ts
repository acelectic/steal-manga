import { Document } from 'mongodb'

export interface IMangaWebData extends Document {
  id: string
  name: string
  link: string
}

export interface IUpdateMangaWebPayload {
  mangaWebs: IMangaWebData[]
}

export interface IMangaUpload extends Document {
  project_name: string
  project_drive_id: string
  cartoon_id: string
  cartoon_name: string
  cartoon_drive_id: string
  manga_chapter_name: string
  manga_chapter_drive_id: string
  created_time: string
  modified_by_me_time: string
  viewed_by_me: boolean
  downloaded: number
}
