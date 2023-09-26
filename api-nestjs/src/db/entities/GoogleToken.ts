import { ModelDefinition, Prop, Schema, SchemaFactory } from '@nestjs/mongoose'
import { HydratedDocument } from 'mongoose'

export type GoogleTokenDocument = HydratedDocument<GoogleToken>

export interface IGoogleToken {
  token: string
  refresh_token: string
  token_uri: string
  client_id: string
  client_secret: string
  scopes: string[]
  expiry: string
}

@Schema({
  collection: 'google_tokens',
})
export class GoogleToken implements IGoogleToken {
  @Prop({
    required: true,
  })
  token: string

  @Prop({
    required: true,
  })
  refresh_token: string

  @Prop({
    required: true,
  })
  token_uri: string

  @Prop({
    required: true,
  })
  client_id: string

  @Prop({
    required: true,
  })
  client_secret: string

  @Prop({
    type: [String],
    required: true,
  })
  scopes: string[]

  @Prop({
    required: true,
  })
  expiry: string
}

export const GoogleTokenSchema = SchemaFactory.createForClass(GoogleToken)
export const GoogleTokenModelDefinition: ModelDefinition = {
  name: GoogleToken.name,
  schema: GoogleTokenSchema,
}
