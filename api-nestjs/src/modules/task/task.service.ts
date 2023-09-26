import { Injectable } from '@nestjs/common'
import { Timeout } from '@nestjs/schedule'
import { MangaDownloadService } from '../manga-download/manga-download.service'

@Injectable()
export class TaskService {
  constructor(private readonly mangaDownloadService: MangaDownloadService) {}

  @Timeout(2 * 1000)
  async test() {
    // await this.mangaDownloadService.downloadMangaByProject({
    //   projectName: EnumMangaConfigProjectName.MY_NOVEL,
    // })
    // const mangaConfigs = await this.mangaConfigService.findAll({
    //   project_name: EnumMangaConfigProjectName.MY_NOVEL,
    //   disabled: false,
    // })
    // for (const mangaConfig of mangaConfigs) {
    //   console.debug(mangaConfig.cartoon_name)
    //   await this.mangaPythonServiceService.downloadMangaOne(
    //     mangaConfig.cartoon_id,
    //   )
    // }
  }
}
