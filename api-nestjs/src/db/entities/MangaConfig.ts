import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose'
import { HydratedDocument } from 'mongoose'

export type MangaConfigDocument = HydratedDocument<MangaConfig>

export enum EnumMangaConfigProjectName {
  MAN_MIRROR = 'man-mirror',
  MY_NOVEL = 'my-novel',
}

export interface IMangaConfig {
  cartoon_name: string
  cartoon_id: string
  latest_chapter: number
  max_chapter: number
  disabled: boolean
  downloaded: number
  project_name: EnumMangaConfigProjectName
  cartoon_drive_id: string
}

@Schema({
  collection: 'manga_configs',
})
export class MangaConfig implements IMangaConfig {
  @Prop({
    enum: EnumMangaConfigProjectName,
    required: true,
  })
  project_name: EnumMangaConfigProjectName

  @Prop({
    required: true,
  })
  cartoon_name: string

  @Prop({
    required: true,
    unique: true,
  })
  cartoon_id: string

  @Prop({
    type: Number,
    required: true,
  })
  latest_chapter: number

  @Prop(Number)
  max_chapter: number

  @Prop(Boolean)
  disabled: boolean

  @Prop(Number)
  downloaded: number

  @Prop()
  cartoon_drive_id: string
}

export const MangaConfigSchema = SchemaFactory.createForClass(MangaConfig)
