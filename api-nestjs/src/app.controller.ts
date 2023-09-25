import { Controller, Get, HttpCode } from '@nestjs/common'
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
}
