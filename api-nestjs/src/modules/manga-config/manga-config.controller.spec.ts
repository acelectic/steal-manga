import { Test, TestingModule } from '@nestjs/testing'
import { MangaConfigController } from './manga-config.controller'
import { MangaConfigService } from './manga-config.service'

describe('MangaConfigController', () => {
  let controller: MangaConfigController

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [MangaConfigController],
      providers: [MangaConfigService],
    }).compile()

    controller = module.get<MangaConfigController>(MangaConfigController)
  })

  it('should be defined', () => {
    expect(controller).toBeDefined()
  })
})
