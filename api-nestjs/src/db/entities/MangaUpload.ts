import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose'
import { HydratedDocument } from 'mongoose'

export type MangaUploadDocument = HydratedDocument<MangaUpload>

export interface IMangaUpload {
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

@Schema({
  collection: 'manga_uploads',
})
export class MangaUpload implements IMangaUpload {
  @Prop({
    required: true,
  })
  project_name: string

  @Prop({
    required: true,
  })
  project_drive_id: string

  @Prop({
    required: true,
  })
  cartoon_id: string

  @Prop({
    required: true,
  })
  cartoon_name: string

  @Prop({
    required: true,
  })
  cartoon_drive_id: string

  @Prop({
    required: true,
  })
  manga_chapter_name: string

  @Prop({
    required: true,
  })
  manga_chapter_drive_id: string

  @Prop(Date)
  created_time: string

  @Prop(Date)
  modified_by_me_time: string

  @Prop(Boolean)
  viewed_by_me: boolean

  @Prop(Number)
  downloaded: number
}

export const MangaUploadSchema = SchemaFactory.createForClass(MangaUpload)
