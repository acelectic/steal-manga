import { Global, Module } from '@nestjs/common'
import { MangaPythonServiceController } from './manga-python-service.controller'
import { MangaPythonService } from './manga-python-service.service'

@Global()
@Module({
  controllers: [MangaPythonServiceController],
  providers: [MangaPythonService],
  exports: [MangaPythonService],
})
export class MangaPythonServiceModule {}
