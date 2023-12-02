import { ModelDefinition, Prop, Schema, SchemaFactory } from '@nestjs/mongoose'
import { HydratedDocument } from 'mongoose'

export type LineUserDocument = HydratedDocument<LineUser>

export interface ILineUser {
  name: string
  userId: string
  isActive: boolean
}

@Schema({
  collection: 'line_users',
})
export class LineUser implements ILineUser {
  @Prop({
    required: true,
  })
  name: string

  @Prop({
    required: true,
  })
  userId: string

  @Prop({
    type: Boolean,
    required: true,
    default: false,
  })
  isActive: boolean
}

export const LineUserSchema = SchemaFactory.createForClass(LineUser)
export const LineUserModelDefinition: ModelDefinition = {
  name: LineUser.name,
  schema: LineUserSchema,
}
