import { Injectable } from '@nestjs/common'
import { MangaConfigService } from '../manga-config/manga-config.service'

@Injectable()
export class TaskService {
  constructor(private readonly mangaConfigService: MangaConfigService) {}

  // @Timeout(5 * 1000)
  // async test() {
  //   console.log('test')
  //   const result = await this.mangaConfigService.findAll()
  //   console.log({ result })
  // }
}
