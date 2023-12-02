import { MessagingApiClient } from '@line/bot-sdk/dist/messaging-api/api'
import { Processor, WorkerHost } from '@nestjs/bullmq'
import { Job } from 'bullmq'
import appConfig from '../../../config/app-config'
import { LineService } from '../../line/line.service'
import { DownLoadMangaOneParamsDto } from '../../manga-download/dto/download-manga-one'
import { SendLineMessageProcessorConstants } from '../task.constants'

@Processor(SendLineMessageProcessorConstants.PROCESSOR_NAME)
export class SendLineMessageProcessor extends WorkerHost {
  client = new MessagingApiClient({
    channelAccessToken: appConfig.LINE_CHANNEL_ACCESS_TOKEN,
  })

  constructor(private readonly lineService: LineService) {
    super()
  }

  process(job: Job<any, any, SendLineMessageProcessorConstants>) {
    switch (job.name) {
      case SendLineMessageProcessorConstants.SEND_MESSAGE:
        return this.sendMessage(job)
      default:
        throw new Error(`can not handle job [${job.name}]`)
    }
  }

  async sendMessage(job: Job<DownLoadMangaOneParamsDto>) {
    const messages = await this.lineService.getMessageCanSend()
    job.log(`messages: ${messages.length}`)

    for (const message of messages) {
      await this.client.pushMessage({
        to: message.userId,
        messages: [
          {
            type: 'text',
            text: message.message,
          },
        ],
      })
      await this.lineService.markLineMessageSent([message._id.toString()])
    }
  }
}
