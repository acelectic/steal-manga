import { Module } from '@nestjs/common'
import { MongooseModule } from '@nestjs/mongoose'
import { MangaConfig, MangaConfigSchema } from '../../db/entities/MangaConfig'
import { MangaConfigController } from './manga-config.controller'
import { MangaConfigService } from './manga-config.service'

@Module({
  imports: [
    MongooseModule.forFeature([
      {
        name: MangaConfig.name,
        schema: MangaConfigSchema,
      },
    ]),
  ],
  controllers: [MangaConfigController],
  providers: [MangaConfigService],
  exports: [MangaConfigService],
})
export class MangaConfigModule {}
