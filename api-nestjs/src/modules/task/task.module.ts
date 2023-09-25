import { BullModule } from '@nestjs/bullmq'
import { Module, Provider } from '@nestjs/common'

import appConfig from '../../config/app-config'
import { MangaConfigModule } from '../manga-config/manga-config.module'
import { BullBoardProvider } from './bull-board.provider'
import { TaskCommand } from './task.command'
import { TaskController } from './task.controller'
import { TaskService } from './task.service'

const providers: Provider[] = [BullBoardProvider, TaskCommand]
if (appConfig.IS_WORKER) {
  providers.push(...[TaskService])
}

@Module({
  imports: [BullModule.registerQueue(), MangaConfigModule],
  providers,
  controllers: [TaskController],
  exports: [TaskCommand],
})
export class TaskModule {}
