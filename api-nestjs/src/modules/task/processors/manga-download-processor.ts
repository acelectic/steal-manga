import { Processor, WorkerHost } from '@nestjs/bullmq'
import { Job } from 'bullmq'
import { DownLoadMangaOneParamsDto } from '../../manga-download/dto/download-manga-one'
import { MangaDownloadService } from '../../manga-download/manga-download.service'
import { MangaDownloadConstants } from '../task.constants'

@Processor(MangaDownloadConstants.PROCESSOR_NAME)
export class MangaDownloadProcessor extends WorkerHost {
  constructor(private readonly mangaDownloadService: MangaDownloadService) {
    super()
  }

  process(job: Job<any, any, MangaDownloadConstants>) {
    switch (job.name) {
      case MangaDownloadConstants.DOWNLOAD:
        return this.downloadMangaByProject(job)
      default:
        throw new Error(`can not handle job [${job.name}]`)
    }
  }

  async downloadMangaByProject(job: Job<DownLoadMangaOneParamsDto>) {
    const { data } = job
    const onProgress = async (progress: number) => {
      await job.updateProgress(progress)
    }
    return await this.mangaDownloadService.performDownloadMangaByProject(
      data,
      onProgress,
    )
  }
}
