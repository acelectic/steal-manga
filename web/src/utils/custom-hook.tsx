'use client'

import { useQuery, useQueryClient } from '@tanstack/react-query'
import { TablePaginationConfig } from 'antd'
import { chain } from 'lodash'
import { usePathname, useRouter, useSearchParams } from 'next/navigation'
import { stringify } from 'qs'
import { useCallback, useContext, useEffect, useMemo } from 'react'
import { SSEContext } from '../components/providers/SseProvider'

interface IPaginateHandleOptions {
  prefix?: string
  defaultPage?: number
  defaultPageSize?: number
  paginationOptions?: Omit<TablePaginationConfig, 'current' | 'pageSize'>
}
export const usePaginationOptions = (options: IPaginateHandleOptions): TablePaginationConfig => {
  const { prefix, defaultPage = 1, defaultPageSize = 50, paginationOptions } = options
  const {
    pageSizeOptions = [5, 10, 20, 50],
    onChange,
    ...restPaginationOptions
  } = paginationOptions || {}

  const router = useRouter()
  const searchParams = useSearchParams()
  const pathname = usePathname()

  const pageKey = useMemo(() => {
    const rawKey = chain([prefix, 'page']).compact().join('-').value()
    return btoa(rawKey)
  }, [prefix])

  const pageSizeKey = useMemo(() => {
    const rawKey = chain([prefix, 'page-size']).compact().join('-').value()
    return btoa(rawKey)
  }, [prefix])

  const current = useMemo(
    () =>
      chain(searchParams.get(pageKey) || defaultPage)
        .toNumber()
        .value(),
    [defaultPage, pageKey, searchParams],
  )

  const pageSize = useMemo(
    () =>
      chain(searchParams.get(pageSizeKey) || defaultPageSize)
        .toNumber()
        .value(),
    [defaultPageSize, pageSizeKey, searchParams],
  )

  const queryParams = useMemo(() => {
    const query: Record<string, any> = {}
    searchParams.forEach((v, k) => {
      query[k] = v
    })
    return query
  }, [searchParams])

  const handleChange = useCallback(
    (newPage: number, newPageSize: number) => {
      router.replace(
        pathname +
          '?' +
          stringify({
            ...queryParams,
            [pageKey]: newPageSize !== pageSize ? 1 : newPage,
            [pageSizeKey]: newPageSize,
          }),
      )

      onChange?.(newPage, newPageSize)
    },
    [onChange, pageKey, pageSize, pageSizeKey, pathname, queryParams, router],
  )

  return useMemo(() => {
    return {
      current,
      pageSize,
      pageSizeOptions,
      onChange: handleChange,
      ...restPaginationOptions,
    }
  }, [current, handleChange, pageSize, pageSizeOptions, restPaginationOptions])
}

export const useSse = <T extends any>(url: string, enabled = false) => {
  const queryKey = useMemo(() => ['sse', url], [url])
  const query = useQuery<T>(queryKey)
  const queryClient = useQueryClient()
  const [, , getEventSource, removeEventSource] = useContext(SSEContext)

  useEffect(() => {
    let eventSource: EventSource
    if (url && enabled) {
      eventSource = getEventSource(url)
      eventSource.onmessage = ({ data: dataString }) => {
        const data = JSON.parse(dataString)
        queryClient.setQueryData(queryKey, data)
      }
      eventSource.onerror = () => {
        eventSource.close()
        removeEventSource(url)
      }
    }

    if (!enabled) {
      removeEventSource(url)
    }
    return () => {
      eventSource?.close()
      removeEventSource(url)
    }
  }, [enabled, getEventSource, queryClient, queryKey, removeEventSource, url])

  return query
}
