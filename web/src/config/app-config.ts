import { get } from 'lodash'
import config from 'next/config'

const getAppConfig = <T extends any = string>(key: string, defaultValue?: T) => {
  const { serverRuntimeConfig, publicRuntimeConfig } = config as any
  // console.log({ serverRuntimeConfig, publicRuntimeConfig })
  return (get(serverRuntimeConfig || {}, key) ||
    get(publicRuntimeConfig || {}, key) ||
    get(process.env || {}, key) ||
    defaultValue) as T
}

export const appConfig = {
  API_HOST: getAppConfig<string>('API_HOST', ''),
  NEXT_PUBLIC_LOG_ROCKET_APP_ID: getAppConfig<string>('NEXT_PUBLIC_LOG_ROCKET_APP_ID'),
  KOYEB_API_HOST: getAppConfig<string>('KOYEB_API_HOST', ''),
  KOYEB_API_SERVICE_ID: getAppConfig<string>('KOYEB_API_SERVICE_ID', ''),
  KOYEB_API_KEY: getAppConfig<string>('KOYEB_API_KEY', ''),
  DB_USERNAME: getAppConfig<string>('DB_USERNAME', ''),
  DB_PASSWORD: getAppConfig<string>('DB_PASSWORD', ''),
  DB_NAME: getAppConfig<string>('DB_NAME', ''),
}
