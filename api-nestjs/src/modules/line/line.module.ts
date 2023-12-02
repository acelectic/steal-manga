import { Module } from '@nestjs/common'
import { MongooseModule } from '@nestjs/mongoose'
import { LineMessageModelDefinition } from '../../db/entities/LineMessage'
import { LineUserModelDefinition } from '../../db/entities/LineUser'
import { LineController } from './line.controller'
import { LineService } from './line.service'

@Module({
  imports: [
    MongooseModule.forFeature([
      LineUserModelDefinition,
      LineMessageModelDefinition,
    ]),
  ],
  controllers: [LineController],
  providers: [LineService],
  exports: [LineService],
})
export class LineModule {}
