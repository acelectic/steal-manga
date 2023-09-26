import { QueueOptions } from 'bullmq'
import appConfig from './app-config'

export const bullConfig: QueueOptions = {
  connection: {
    host: appConfig.REDIS_HOST,
    port: Number(appConfig.REDIS_PORT),
  },
  prefix: appConfig.REDIS_PREFIX,
  defaultJobOptions: {
    removeOnComplete: 1000,
  },
}
