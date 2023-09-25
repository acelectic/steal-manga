import { BullModule } from '@nestjs/bullmq'
import { Module, RequestMethod } from '@nestjs/common'
import { ConfigModule } from '@nestjs/config'
import { MongooseModule } from '@nestjs/mongoose'
import { ScheduleModule } from '@nestjs/schedule'
import { LoggerModule } from 'nestjs-pino'
import { AppController } from './app.controller'
import { AppService } from './app.service'
import appConfig, { validationEnvSchema } from './config/app-config'
import { dbConfig } from './config/db-config'
import { MangaConfigModule } from './modules/manga-config/manga-config.module'
import { TaskModule } from './modules/task/task.module'

@Module({
  imports: [
    ConfigModule.forRoot({
      validationSchema: validationEnvSchema,
    }),
    MongooseModule.forRootAsync(dbConfig),
    ScheduleModule.forRoot(),
    BullModule.forRoot({
      connection: {
        host: appConfig.REDIS_HOST,
        port: Number(appConfig.REDIS_PORT),
      },
      prefix: appConfig.REDIS_PREFIX,
      defaultJobOptions: {
        removeOnComplete: 1000,
      },
    }),
    LoggerModule.forRoot({
      pinoHttp: {
        level: 'info',
        redact: {
          paths: ['req.body.password', 'req.headers.authorization'],
          censor: '********',
        },
        serializers: {
          req(req) {
            req.body = req.raw.body
            return req
          },
        },
      },
      exclude: [{ method: RequestMethod.GET, path: '/api/v1/health' }],
    }),

    // common module
    TaskModule,

    // modules
    MangaConfigModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
