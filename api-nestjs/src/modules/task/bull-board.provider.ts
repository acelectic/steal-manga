import { createBullBoard } from '@bull-board/api'
import { BullMQAdapter } from '@bull-board/api/bullMQAdapter'
import { ExpressAdapter } from '@bull-board/express'
import { InjectQueue } from '@nestjs/bullmq'
import { Injectable } from '@nestjs/common'
import { Queue } from 'bullmq'
import { MangaDownloadConstants } from './task.constants'

export const bullServerAdapter = new ExpressAdapter()

@Injectable()
export class BullBoardProvider {
  constructor(
    @InjectQueue(MangaDownloadConstants.PROCESSOR_NAME)
    private readonly mangaDownloadQueue: Queue,
  ) {
    createBullBoard({
      queues: [new BullMQAdapter(this.mangaDownloadQueue)],
      serverAdapter: bullServerAdapter,
    })
  }
}
