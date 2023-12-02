import { BullModule } from '@nestjs/bullmq'
import { Global, Module, Provider } from '@nestjs/common'

import appConfig from '../../config/app-config'
import { LineModule } from '../line/line.module'
import { MangaConfigModule } from '../manga-config/manga-config.module'
import { MangaDownloadModule } from '../manga-download/manga-download.module'
import { BullBoardProvider } from './bull-board.provider'
import { MangaDownloadProcessor } from './processors/manga-download-processor'
import { SendLineMessageProcessor } from './processors/send-line-message-processor'
import { TaskCommand } from './task.command'
import {
  MangaDownloadConstants,
  SendLineMessageProcessorConstants,
} from './task.constants'
import { TaskController } from './task.controller'
import { TaskService } from './task.service'

const providers: Provider[] = [BullBoardProvider, TaskCommand]
if (appConfig.IS_WORKER) {
  providers.push(
    ...[TaskService, MangaDownloadProcessor, SendLineMessageProcessor],
  )
}

@Global()
@Module({
  imports: [
    BullModule.registerQueue(
      {
        name: MangaDownloadConstants.PROCESSOR_NAME,
      },
      {
        name: SendLineMessageProcessorConstants.PROCESSOR_NAME,
      },
    ),
    MangaConfigModule,
    MangaDownloadModule,
    LineModule,
  ],
  providers,
  controllers: [TaskController],
  exports: [TaskCommand],
})
export class TaskModule {}
