import { BullModule } from '@nestjs/bullmq'
import { Global, Module, Provider } from '@nestjs/common'

import appConfig from '../../config/app-config'
import { MangaConfigModule } from '../manga-config/manga-config.module'
import { MangaDownloadModule } from '../manga-download/manga-download.module'
import { BullBoardProvider } from './bull-board.provider'
import { MangaDownloadProcessor } from './processors/manga-download-processor'
import { TaskCommand } from './task.command'
import { MangaDownloadConstants } from './task.constants'
import { TaskController } from './task.controller'
import { TaskService } from './task.service'

const providers: Provider[] = [BullBoardProvider, TaskCommand]
if (appConfig.IS_WORKER) {
  providers.push(...[TaskService, MangaDownloadProcessor])
}

@Global()
@Module({
  imports: [
    BullModule.registerQueue({
      name: MangaDownloadConstants.PROCESSOR_NAME,
    }),
    MangaConfigModule,
    MangaDownloadModule,
  ],
  providers,
  controllers: [TaskController],
  exports: [TaskCommand],
})
export class TaskModule {}
