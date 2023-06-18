'use client'

import { ConfigProvider } from 'antd'
import React from 'react'
import { PropsWithChildren } from 'react'
import { StyleProvider, createCache, extractStyle } from '@ant-design/cssinjs'
import { useServerInsertedHTML } from 'next/navigation'

export const AntdProvider = (props: PropsWithChildren) => {
  const cache = createCache()
  // const key = 'custom'
  // const emotionCache = createEmotionCache({ key })
  // const dehydratedState = useDehydratedState()
  useServerInsertedHTML(() => {
    return (
      <script
        dangerouslySetInnerHTML={{
          __html: `</script>${extractStyle(cache)}<script>`,
        }}
      />
    )
  })

  return (
    <StyleProvider cache={cache}>
      <ConfigProvider
        form={{
          scrollToFirstError: true,
        }}
      >
        {props.children}
      </ConfigProvider>
    </StyleProvider>
  )
}
