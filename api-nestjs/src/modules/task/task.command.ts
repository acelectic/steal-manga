import { InjectQueue } from '@nestjs/bullmq'
import { Injectable } from '@nestjs/common'
import { Queue } from 'bullmq'
import { DownLoadMangaOneParamsDto } from '../manga-download/dto/download-manga-one'
import { MangaDownloadConstants } from './task.constants'

@Injectable()
export class TaskCommand {
  constructor(
    @InjectQueue(MangaDownloadConstants.PROCESSOR_NAME)
    private readonly mangaDownloadQueue: Queue,
  ) {}

  async downloadMangaByProject(params: DownLoadMangaOneParamsDto) {
    return this.mangaDownloadQueue.add(MangaDownloadConstants.DOWNLOAD, params)
  }
}
