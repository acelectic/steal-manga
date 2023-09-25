import { createBullBoard } from '@bull-board/api'
import { ExpressAdapter } from '@bull-board/express'
import { Injectable } from '@nestjs/common'

export const bullServerAdapter = new ExpressAdapter()

@Injectable()
export class BullBoardProvider {
  constructor() {
    createBullBoard({
      queues: [],
      serverAdapter: bullServerAdapter,
    })
  }
}
