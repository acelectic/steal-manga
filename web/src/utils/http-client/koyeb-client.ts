import { AxiosError, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import dayjs from 'dayjs'
import { BaseHttpClient } from './base-http-client'
import { appConfig } from '../../config/app-config'
import path from 'path'

class KoyebClient extends BaseHttpClient {
  constructor(version = 'v1') {
    super({
      baseURL: path.join(appConfig.KOYEB_API_HOST, version),
      // withCredentials: true,
    })
  }

  protected async onRequest(
    request: InternalAxiosRequestConfig<any>,
  ): Promise<InternalAxiosRequestConfig<any>> {
    // const accessToken = localStorage.getItem('accessToken')
    // if (accessToken) {
    //   request.headers.Authorization = 'Bearer ' + accessToken
    // }
    request.headers.Authorization = 'Bearer ' + appConfig.KOYEB_API_KEY

    console.log(request.baseURL, request.url)

    return request
  }

  protected async onResponse(response: AxiosResponse<any, any>): Promise<AxiosResponse<any, any>> {
    response.data = response.data?.data || response.data
    return response
  }

  protected onError(
    error: AxiosError<unknown, any>,
  ): Promise<AxiosRequestConfig<any> | AxiosError<unknown, any>> {
    console.log({ error: error })
    return Promise.reject(error)
  }

  protected normalizeRequestData(value: any) {
    if (value instanceof Date) {
      return value.toISOString()
    }
    if (dayjs.isDayjs(value)) {
      return value.toISOString()
    }
    return value
  }
}

export const koyebClient = new KoyebClient()
