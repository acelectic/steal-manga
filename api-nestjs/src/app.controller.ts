import { Body, Controller, Get, HttpCode, Post } from '@nestjs/common'
import { AppService } from './app.service'
import appConfig from './config/app-config'

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get('/health')
  @HttpCode(200)
  health() {
    return { statusCode: 200, status: 'Ok !!', version: appConfig.VERSION }
  }

  @Post('qr-code/callback')
  qrCodeCallback(@Body() params) {
    console.log({ params })
  }
}
