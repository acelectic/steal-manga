import { camelizeKeys } from 'humps'
import { appConfig } from '../../config/app-config'

export const fetchMangaUpdated = async () => {
  const response = await fetch(appConfig.API_HOST + '/api/v1/fetch-manga-updated', {
    method: 'POST',
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    headers: {
      'Content-Type': 'application/json',
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
  return camelizeKeys(await response.json())
}
