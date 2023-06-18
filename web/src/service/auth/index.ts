import { camelizeKeys } from 'humps'
import path from 'path'
import { BASE_API_URL } from '../shared'
import { IGetAuthGoogleStatusResponse, IGetAuthGoogleUrlResponse } from './types'

const AUTH_GOOGLE_DRIVE = path.join(BASE_API_URL, 'auth-google-drive')
export const getAuthGoogleStatus = async (options?: RequestInit) => {
  const response = await fetch(AUTH_GOOGLE_DRIVE, options)
  const responseData = await response.json()
  return camelizeKeys(responseData) as IGetAuthGoogleStatusResponse
}

export const getAuthGoogleUrl = async () => {
  const response = await fetch(AUTH_GOOGLE_DRIVE, {
    method: 'POST',
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    headers: {
      'Content-Type': 'application/json',
    },
  })
  return camelizeKeys(await response.json()) as IGetAuthGoogleUrlResponse
}
