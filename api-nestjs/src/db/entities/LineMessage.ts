import { ModelDefinition, Prop, Schema, SchemaFactory } from '@nestjs/mongoose'
import { HydratedDocument } from 'mongoose'

export type LineMessageDocument = HydratedDocument<LineMessage>

export interface ILineMessage {
  userId: string
  message: string
  isSent: boolean
}

@Schema({
  collection: 'line_users',
})
export class LineMessage implements ILineMessage {
  @Prop({
    required: true,
  })
  userId: string

  @Prop({
    required: true,
  })
  message: string

  @Prop({
    type: Boolean,
    required: true,
    default: false,
  })
  isSent: boolean
}

export const LineMessageSchema = SchemaFactory.createForClass(LineMessage)
export const LineMessageModelDefinition: ModelDefinition = {
  name: LineMessage.name,
  schema: LineMessageSchema,
}
