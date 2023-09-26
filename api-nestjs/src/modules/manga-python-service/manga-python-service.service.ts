import { Injectable } from '@nestjs/common'
import { pythonApi } from '../../utils/http-clients/python-api-client'

@Injectable()
export class MangaPythonService {
  async downloadMangaOne(mangaConfigId: string) {
    const { data } = await pythonApi.post(
      `api/v1/cartoons/${mangaConfigId}/download`,
    )
    return data
  }
}
