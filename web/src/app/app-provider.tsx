'use client'

import { Hydrate, QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ConfigProvider } from 'antd'
import React from 'react'
import { PropsWithChildren } from 'react'
import { StyleProvider, createCache, extractStyle } from '@ant-design/cssinjs'
// import { useDehydratedState } from 'use-dehydrated-state'
// import { RemixBrowser } from '@remix-run/react'

export const AppProvider = (props: PropsWithChildren) => {
  const [queryClient] = React.useState(() => new QueryClient())
  const cache = createCache()

  // const dehydratedState = useDehydratedState()

  return (
    <QueryClientProvider client={queryClient}>
      <StyleProvider cache={cache}>
        <ConfigProvider
          form={{
            scrollToFirstError: true,
          }}
        >
          {/* <style data-test="extract" dangerouslySetInnerHTML={{ __html: extractStyle(cache) }} /> */}
          {/* <Hydrate state={dehydratedState}>{props.children}</Hydrate> */}
          {props.children}
        </ConfigProvider>
      </StyleProvider>
    </QueryClientProvider>
  )
}
