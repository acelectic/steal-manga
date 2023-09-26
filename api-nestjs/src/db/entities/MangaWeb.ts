import { ModelDefinition, Prop, Schema, SchemaFactory } from '@nestjs/mongoose'
import { HydratedDocument } from 'mongoose'

export type MangaWebDocument = HydratedDocument<MangaWeb>

export interface IMangaWeb {
  name: string
  link: string
}

@Schema({
  collection: 'manga_webs',
})
export class MangaWeb implements IMangaWeb {
  @Prop({
    required: true,
  })
  name: string

  @Prop({
    required: true,
  })
  link: string
}

export const MangaWebSchema = SchemaFactory.createForClass(MangaWeb)
export const MangaWebModelDefinition: ModelDefinition = {
  name: MangaWeb.name,
  schema: MangaWebSchema,
}
