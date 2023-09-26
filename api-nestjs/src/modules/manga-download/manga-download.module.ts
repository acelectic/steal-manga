import { Module } from '@nestjs/common'
import { MongooseModule } from '@nestjs/mongoose'
import { MangaConfigModelDefinition } from '../../db/entities/MangaConfig'
import { MangaDownloadController } from './manga-download.controller'
import { MangaDownloadService } from './manga-download.service'

@Module({
  imports: [MongooseModule.forFeature([MangaConfigModelDefinition])],
  controllers: [MangaDownloadController],
  providers: [MangaDownloadService],
  exports: [MangaDownloadService],
})
export class MangaDownloadModule {}
