import { Injectable } from '@nestjs/common'
import { InjectModel } from '@nestjs/mongoose'
import { FilterQuery, Model } from 'mongoose'
import { MangaConfig } from '../../db/entities/MangaConfig'

@Injectable()
export class MangaConfigService {
  constructor(
    @InjectModel(MangaConfig.name) private mangaConfigModel: Model<MangaConfig>,
  ) {}

  async findAll(filter?: FilterQuery<MangaConfig>) {
    return await this.mangaConfigModel.find(filter)
  }
}
