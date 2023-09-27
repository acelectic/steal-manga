import { Module } from '@nestjs/common'
import { MongooseModule } from '@nestjs/mongoose'
import { MangaConfigModelDefinition } from '../../db/entities/MangaConfig'
import { MangaUploadModelDefinition } from '../../db/entities/MangaUpload'
import { MangaWebModelDefinition } from '../../db/entities/MangaWeb'
import { MangaDownloadController } from './manga-download.controller'
import { MangaDownloadService } from './manga-download.service'

@Module({
  imports: [
    MongooseModule.forFeature([
      MangaConfigModelDefinition,
      MangaUploadModelDefinition,
      MangaWebModelDefinition,
    ]),
  ],
  controllers: [MangaDownloadController],
  providers: [MangaDownloadService],
  exports: [MangaDownloadService],
})
export class MangaDownloadModule {}
