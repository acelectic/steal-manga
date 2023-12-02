import { BullModule } from '@nestjs/bullmq'
import { CacheModule } from '@nestjs/cache-manager'
import { Module } from '@nestjs/common'
import { ConfigModule } from '@nestjs/config'
import { EventEmitterModule } from '@nestjs/event-emitter'
import { MongooseModule } from '@nestjs/mongoose'
import { ScheduleModule } from '@nestjs/schedule'
import { LoggerModule } from 'nestjs-pino'
import { AppController } from './app.controller'
import { AppService } from './app.service'
import { appConfigModuleOptions } from './config/app-config'
import { bullConfig } from './config/bull-config'
import {
  appCacheModuleConfig,
  cacheModuleConfig,
} from './config/cache-module-config'
import { dbConfig } from './config/db-config'
import { httpLoggerConfig } from './config/http-logger-config'
import { LineModule } from './modules/line/line.module'
import { MangaConfigModule } from './modules/manga-config/manga-config.module'
import { MangaDownloadModule } from './modules/manga-download/manga-download.module'
import { MangaPythonServiceModule } from './modules/manga-python-service/manga-python-service.module'
import { TaskModule } from './modules/task/task.module'

@Module({
  imports: [
    ConfigModule.forRoot(appConfigModuleOptions),
    MongooseModule.forRootAsync(dbConfig),
    ScheduleModule.forRoot(),
    BullModule.forRoot(bullConfig),
    LoggerModule.forRoot(httpLoggerConfig),
    CacheModule.register(cacheModuleConfig),
    EventEmitterModule.forRoot(),

    // common module
    TaskModule,
    MangaPythonServiceModule,
    appCacheModuleConfig,

    // service modules
    MangaConfigModule,
    MangaDownloadModule,
    LineModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
