'use client'

import { TablePaginationConfig } from 'antd'
import { chain } from 'lodash'
import { useRouter, usePathname, useSearchParams } from 'next/navigation'
import { stringify } from 'qs'
import { useMemo } from 'react'

export const usePaginationHandle = (prefix?: string): TablePaginationConfig => {
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
    const current = chain(searchParams.get(pageKey) || 1)
      .toNumber()
      .value()
    const pageSize = chain(searchParams.get(pageSizeKey) || 50)
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
    }
  }, [pathname, prefix, router, searchParams])
}
