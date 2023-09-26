/* eslint-disable @typescript-eslint/no-explicit-any */
import axios, {
  AxiosError,
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from 'axios'
import dayjs from 'dayjs'
import { get, set } from 'lodash'
import qs from 'qs'

export enum ContentType {
  X_WWW_FORM_URLENCODED = 'application/x-www-form-urlencoded',
  JSON = 'application/json',
  FORM_DATA = 'multipart/form-data',
}

export const getContentTypeHeader = (contentType: ContentType) => {
  return { 'Content-Type': contentType }
}

export class BaseHttpClient {
  private readonly ax: AxiosInstance

  constructor(config: AxiosRequestConfig) {
    this.ax = axios.create(config)
    this.ax.interceptors.request.use(async (request) => {
      set(
        request,
        'headers.Content-Type',
        get(request, 'headers.Content-Type', ContentType.JSON),
      )
      if (request.data) {
        request.data = this.deepLoop(request.data, this.normalizeRequestData)
      }

      if (request.headers?.['Content-Type'] === ContentType.FORM_DATA) {
        this.parseDataToFormData(request)
      } else if (
        request.headers?.['Content-Type'] === ContentType.X_WWW_FORM_URLENCODED
      ) {
        this.parseDataToString(request)
      }
      return this.onRequest(request)
    })
    this.ax.interceptors.response.use(
      async (response) => {
        return this.onResponse(
          // this.deepLoop(response, this.normalizeResponseData),
          response,
          response,
        )
      },
      async (error: AxiosError) => {
        if (error.response?.data && error.response.data instanceof Blob) {
          let errorString = await error.response.data.text()
          try {
            errorString = JSON.parse(errorString)
          } catch {}
          error.response.data = errorString
        }
        return this.onError(error)
      },
    )
  }

  private parseDataToString(request: AxiosRequestConfig) {
    if (request.data) {
      request.data = qs.stringify(request.data)
    }
  }

  private parseDataToFormData(request: AxiosRequestConfig) {
    if (request.data && !(request.data instanceof FormData)) {
      const formData = new FormData()
      Object.entries(request.data).forEach(([key, value]: any[]) => {
        if (value !== undefined) {
          if (value instanceof Array) {
            value.forEach((val) => {
              formData.append(`${key}`, val)
            })
          } else {
            formData.append(key, value)
          }
        }
      })
      request.data = formData
    }
  }

  private deepLoop(data: any, func: (d: any) => any): any {
    if (data instanceof Blob) {
      return func(data)
    }
    if (dayjs.isDayjs(data)) {
      return func(data)
    }
    if (data instanceof Date) {
      return func(data)
    }
    if (data instanceof Array) {
      return data.map((d) => this.deepLoop(d, func))
    }
    if (data instanceof Object) {
      const formatData: any = {}
      Object.keys(data).forEach((key) => {
        formatData[key] = this.deepLoop(data[key], func)
      })
      return formatData
    }
    return func(data)
  }

  protected onRequest(
    request: InternalAxiosRequestConfig<any>,
  ): Promise<InternalAxiosRequestConfig<any>> {
    return Promise.resolve(request)
  }
  protected onResponse(
    response: AxiosResponse<any>,
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    rawResponse: AxiosResponse<any>,
  ): Promise<AxiosResponse<any>> {
    return Promise.resolve(response)
  }
  protected onError(error: AxiosError): any {
    return Promise.reject(error)
  }
  protected normalizeRequestData(value: any) {
    return value
  }
  protected normalizeResponseData(value: any) {
    return value
  }

  get<T>(
    url: string,
    config?: AxiosRequestConfig<T>,
  ): Promise<AxiosResponse<T, any>> {
    return this.ax.get<T>(url, config)
  }

  post<T>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig<T>,
  ): Promise<AxiosResponse<T, any>> {
    return this.ax.post<T>(url, data, config)
  }

  put<T>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig,
  ): Promise<AxiosResponse<T, any>> {
    return this.ax.put<T>(url, data, config)
  }

  patch<T>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig,
  ): Promise<AxiosResponse<T, any>> {
    return this.ax.patch<T>(url, data, config)
  }

  delete<T>(
    url: string,
    config?: AxiosRequestConfig<any>,
  ): Promise<AxiosResponse<T, any>> {
    return this.ax.delete<T>(url, config)
  }

  getBlob<T extends Blob>(
    url: string,
    config?: AxiosRequestConfig<Text>,
  ): Promise<AxiosResponse<T, any>> {
    return this.ax.get<T>(url, {
      responseType: 'blob',
      ...config,
    })
  }
}
