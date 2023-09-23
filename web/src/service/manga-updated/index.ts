import { camelizeKeys } from 'humps'
import { appConfig } from '../../config/app-config'
import { IGetMangaUpdatedResponse, IUpdateMangaConfigPayload } from './types'
import path from 'path'
import qs from 'qs'

export const getMangaUpdated = async (options?: RequestInit) => {
  const response = await fetch(
    path.join(appConfig.API_HOST, 'api', 'v1', 'manga-updated') +
      '?' +
      qs.stringify({
        latest_update: 5,
      }),
    {
      cache: 'no-store',
      ...options,
    },
  )
  const responseData = await response.json()
  return camelizeKeys(responseData) as IGetMangaUpdatedResponse
}

export const updateMangaConfig = async (payload: IUpdateMangaConfigPayload) => {
  const response = await fetch('/api/v1/update-config', {
    method: 'POST',
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    // credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'application/json',
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify(payload),
  })
  return camelizeKeys(await response.json()) as IGetMangaUpdatedResponse
}
