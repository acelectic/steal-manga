'use client'

import { useQuery, useQueryClient } from '@tanstack/react-query'
import { TablePaginationConfig } from 'antd'
import { chain } from 'lodash'
import { usePathname, useRouter, useSearchParams } from 'next/navigation'
import { stringify } from 'qs'
import { useEffect, useMemo } from 'react'

interface IPaginateHandleOptions {
  prefix?: string
  defaultPage?: number
  defaultPageSize?: number
  pageSizeOptions?: number[]
}
export const usePaginationHandle = (options: IPaginateHandleOptions): TablePaginationConfig => {
  const {
    prefix,
    defaultPage = 1,
    defaultPageSize = 50,
    pageSizeOptions = [5, 10, 20, 50],
  } = options
  const router = useRouter()
  const searchParams = useSearchParams()
  const pathname = usePathname()

  return useMemo(() => {
    let pageKey = chain([prefix, 'page']).compact().join('-').value()
    pageKey = btoa(pageKey)

    let pageSizeKey = chain([prefix, 'page-size']).compact().join('-').value()
    pageSizeKey = btoa(pageSizeKey)

    const query: Record<string, any> = {}
    searchParams.forEach((v, k) => {
      query[k] = v
    })
    const current = chain(searchParams.get(pageKey) || defaultPage)
      .toNumber()
      .value()
    const pageSize = chain(searchParams.get(pageSizeKey) || defaultPageSize)
      .toNumber()
      .value()

    return {
      current,
      pageSize,
      onChange(newPage, newPageSize) {
        router.replace(
          pathname +
            '?' +
            stringify({
              ...query,
              [pageKey]: newPageSize !== pageSize ? 1 : newPage,
              [pageSizeKey]: newPageSize,
            }),
        )
      },
      pageSizeOptions,
    }
  }, [defaultPage, defaultPageSize, pageSizeOptions, pathname, prefix, router, searchParams])
}

export const useSse = <T extends any>(url: string) => {
  const queryKey = useMemo(() => ['sse', url], [url])
  const query = useQuery<T>(queryKey)
  const queryClient = useQueryClient()

  useEffect(() => {
    let eventSource: EventSource
    if (url) {
      eventSource = new EventSource(url)
      eventSource.onmessage = ({ data: dataString }) => {
        const data = JSON.parse(dataString)
        queryClient.setQueryData(queryKey, data)
      }
    }
    return () => {
      eventSource?.close()
    }
  }, [queryClient, queryKey, url])

  return query
}
