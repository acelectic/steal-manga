import appConfig from '../../config/app-config'
import { BaseHttpClient } from './base-http-client'

class PythonApiClient extends BaseHttpClient {
  constructor() {
    super({
      baseURL: appConfig.MANGA_SERVICE_API_URL,
      withCredentials: true,
    })
  }
}

export const pythonApi = new PythonApiClient()
