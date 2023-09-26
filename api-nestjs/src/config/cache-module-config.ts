import { CacheModuleOptions } from '@nestjs/cache-manager'
import { DynamicModule, Provider } from '@nestjs/common'
import { redisStore } from 'cache-manager-redis-store'
import Redis from 'ioredis'
import appConfig from './app-config'

export const cacheModuleConfig: CacheModuleOptions = {
  isGlobal: true,
  store: {
    create: redisStore as any,
  },
  host: appConfig.REDIS_HOST,
  port: Number(appConfig.REDIS_PORT),
  ttl: 5 * 60, // second
}

export class AppRedisClient extends Redis {}

export const appRedisClientConfig: Provider = {
  provide: AppRedisClient,
  useFactory: () => {
    const redis = new Redis({
      host: appConfig.REDIS_HOST,
      port: appConfig.REDIS_PORT,
      keyPrefix: appConfig.REDIS_PREFIX + ':',
      enableReadyCheck: false,
    })

    return redis
  },
}

class AppCacheModule {}

export const appCacheModuleConfig: DynamicModule = {
  module: AppCacheModule,
  global: true,
  providers: [appRedisClientConfig],
  exports: [appRedisClientConfig],
}
