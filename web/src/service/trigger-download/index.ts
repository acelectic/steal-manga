import { camelizeKeys, decamelizeKeys } from 'humps'
import { ITriggerDownloadPayload } from './types'
import { appConfig } from '../../config/app-config'

export const triggerDownloadManga = async (payload: ITriggerDownloadPayload) => {
  const response = await fetch(appConfig.API_HOST + '/api/v1/download-manga', {
    method: 'POST',
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    headers: {
      'Content-Type': 'application/json',
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify(decamelizeKeys(payload)),
  })
  return camelizeKeys(await response.json())
}
