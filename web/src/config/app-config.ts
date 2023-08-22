import { get } from 'lodash'
import config from 'next/config'

const getConfig2 = <T extends any = string>(key: string) => {
  const { serverRuntimeConfig, publicRuntimeConfig } = config as any
  // console.log({ serverRuntimeConfig, publicRuntimeConfig })
  return (get(serverRuntimeConfig || {}, key, '') ||
    get(publicRuntimeConfig || {}, key, '') ||
    get(process.env || {}, key, '')) as T
}
export const appConfig = {
  API_HOST: getConfig2<string>('API_HOST') || '',
  NEXT_PUBLIC_LOG_ROCKET_APP_ID: getConfig2<string>('NEXT_PUBLIC_LOG_ROCKET_APP_ID'),
}

console.log({ appConfig })
