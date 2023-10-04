import { ModelDefinition, Prop, Schema, SchemaFactory } from '@nestjs/mongoose'
import { Date, HydratedDocument } from 'mongoose'
import { EnumMangaConfigProjectName } from './MangaConfig'

export type MangaUploadDocument = HydratedDocument<MangaUpload>

export interface IMangaUpload {
  project_name: string
  project_drive_id: string
  cartoon_id: string
  cartoon_name: string
  cartoon_drive_id: string
  manga_chapter_name: string
  manga_chapter_drive_id: string
  created_time: Date
  modified_by_me_time: Date
  viewed_by_me: boolean
  downloaded: number
}

@Schema({
  collection: 'manga_uploads',
})
export class MangaUpload implements IMangaUpload {
  @Prop({
    enum: EnumMangaConfigProjectName,
    required: true,
  })
  project_name: EnumMangaConfigProjectName

  @Prop({
    type: String,
    required: true,
  })
  project_drive_id: string

  @Prop({
    type: String,
    required: true,
  })
  cartoon_id: string

  @Prop({
    type: String,
    required: true,
  })
  cartoon_name: string

  @Prop({
    type: String,
    required: true,
  })
  cartoon_drive_id: string

  @Prop({
    type: String,
    required: true,
  })
  manga_chapter_name: string

  @Prop({
    type: String,
    required: true,
  })
  manga_chapter_drive_id: string

  @Prop({
    type: Date,
  })
  created_time: Date

  @Prop({
    type: Date,
  })
  modified_by_me_time: Date

  @Prop(Boolean)
  viewed_by_me: boolean

  @Prop(Number)
  downloaded: number
}

export const MangaUploadSchema = SchemaFactory.createForClass(MangaUpload)
MangaUploadSchema.index(
  {
    cartoon_id: 1,
    manga_chapter_drive_id: 1,
  },
  { unique: true },
)
export const MangaUploadModelDefinition: ModelDefinition = {
  name: MangaUpload.name,
  schema: MangaUploadSchema,
}
