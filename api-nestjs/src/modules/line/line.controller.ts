import { WebhookRequestBody } from '@line/bot-sdk'
import { MessagingApiClient } from '@line/bot-sdk/dist/messaging-api/api'
import {
  Body,
  Controller,
  HttpCode,
  HttpStatus,
  Post,
  Res,
} from '@nestjs/common'
import { ApiTags } from '@nestjs/swagger'
import { Response } from 'express'
import appConfig from '../../config/app-config'
import { LineService } from './line.service'

@ApiTags('line')
@Controller('line')
export class LineController {
  client = new MessagingApiClient({
    channelAccessToken: appConfig.LINE_CHANNEL_ACCESS_TOKEN,
  })

  constructor(private readonly lineService: LineService) {}

  @Post('webhook')
  @HttpCode(HttpStatus.OK)
  async lineWebhook(@Body() params: WebhookRequestBody, @Res() res: Response) {
    console.log(JSON.stringify(params))

    const events = params?.events || []
    for (const event of events) {
      const userId = event.source.userId
      if (event.type === 'follow') {
        const user = await this.client.getProfile(userId)
        await this.lineService.addLineUser(user)
      } else if (event.type === 'unfollow') {
        await this.lineService.userUnFollow(userId)
      }
    }

    // const event = params.events?.[0]
    // const userId = event?.source?.userId
    // const lineId = '225trzbf'
    // if (userId) {
    //   this.client.pushMessage({
    //     to: userId,
    //     messages: [
    //       // {
    //       //   text: event?.type || 'unknown',
    //       //   type: '',
    //       //   altText: 'this is a flex message',
    //       //   contents: {
    //       //     type: 'bubble',
    //       //     body: {
    //       //       type: 'box',
    //       //       layout: 'vertical',
    //       //       contents: [
    //       //         // {
    //       //         //   type: 'text',
    //       //         //   text: 'hello',
    //       //         // },
    //       //         // {
    //       //         //   type: 'text',
    //       //         //   text: 'world',
    //       //         // },
    //       //         {
    //       //           type: 'text',
    //       //           // text: `https://line.me/R/oaMessage/@${lineId}`,
    //       //           text: `https://line.me/R/home/public/profile?id=${lineId}`,
    //       //         },
    //       //       ],
    //       //     },
    //       //   },
    //       // },
    //       {
    //         type: 'text',
    //         // text: `https://line.me/R/oaMessage/@${lineId}`,
    //         text: `https://line.me/R/home/public/profile?id=${lineId}`,
    //       },
    //       // {
    //       //   type: 'text',
    //       //   // text: `https://line.me/R/oaMessage/@${lineId}`,
    //       //   text: `https://line.me/R/home/public/profile?id=${lineId}`,
    //       // },
    //     ],
    //   })
    // }

    res.end()
  }

  @Post('callback')
  async lineLiff(@Body() params: any) {
    const { userId } = params || {}
    console.log({ params })
    // res.redirect('https://line.me/R/oaMessage/1ppas2k')
    if (userId) {
      await this.lineService.addMessage(userId, JSON.stringify(params))
      // this.lineService.addMessage(userId, JSON.stringify(params))
      // await this.client.pushMessage({
      //   to: userId,
      //   messages: [
      //     {
      //       type: 'text',
      //       text: 'hello ' + userId,
      //     },
      //     {
      //       type: 'text',
      //       text: JSON.stringify(params),
      //     },
      //   ],
      // })
    }
  }
}
