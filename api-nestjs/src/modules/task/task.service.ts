import { InjectQueue } from '@nestjs/bullmq'
import { Injectable } from '@nestjs/common'
import { Cron, CronExpression, Timeout } from '@nestjs/schedule'
import { Queue } from 'bullmq'
import { MangaDownloadService } from '../manga-download/manga-download.service'
import { SendLineMessageProcessorConstants } from './task.constants'

@Injectable()
export class TaskService {
  constructor(
    private readonly mangaDownloadService: MangaDownloadService,
    @InjectQueue(SendLineMessageProcessorConstants.PROCESSOR_NAME)
    private readonly sendLineMessageQueue: Queue,
  ) {}

  @Cron(CronExpression.EVERY_5_SECONDS)
  async sendLineMessages() {
    await this.sendLineMessageQueue.add(
      SendLineMessageProcessorConstants.SEND_MESSAGE,
      {},
    )
  }

  @Timeout(2 * 1000)
  async test() {
    // await this.mangaDownloadService.updateLatestSync()
    // await this.mangaDownloadService.downloadMangaByProject({
    //   projectName: EnumMangaConfigProjectName.MY_NOVEL,
    // })
    // const mangaConfigs = await this.mangaConfigService.findAll({
    //   project_name: EnumMangaConfigProjectName.MY_NOVEL,
    //   disabled: false,
    // })
    // for (const mangaConfig of mangaConfigs) {
    //   console.debug(mangaConfig.cartoon_name)
    //   await this.mangaPythonServiceService.downloadMangaOne(
    //     mangaConfig.cartoon_id,
    //   )
    // }
  }
}
