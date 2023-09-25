import { ConfigModule, ConfigService } from '@nestjs/config'
import { MongooseModuleAsyncOptions } from '@nestjs/mongoose'

export const dbConfig: MongooseModuleAsyncOptions = {
  imports: [ConfigModule],
  inject: [ConfigService],
  useFactory: (configService: ConfigService) => {
    const DB_NAME = configService.get('DB_NAME')
    const DB_USERNAME = configService.get('DB_USERNAME')
    const DB_PASSWORD = configService.get('DB_PASSWORD')
    return {
      uri: `mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}@${DB_NAME}.nlqv7lj.mongodb.net/?retryWrites=true&w=majority`,
      dbName: DB_NAME,
    }
  },
}
