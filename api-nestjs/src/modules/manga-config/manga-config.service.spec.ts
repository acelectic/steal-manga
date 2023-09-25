import { Test, TestingModule } from '@nestjs/testing'
import { MangaConfigService } from './manga-config.service'

describe('MangaConfigService', () => {
  let service: MangaConfigService

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [MangaConfigService],
    }).compile()

    service = module.get<MangaConfigService>(MangaConfigService)
  })

  it('should be defined', () => {
    expect(service).toBeDefined()
  })
})
