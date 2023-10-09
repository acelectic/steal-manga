'use client'

import { StyleProvider, createCache, extractStyle } from '@ant-design/cssinjs'
import type Entity from '@ant-design/cssinjs/es/Cache'
import { ConfigProvider } from 'antd'
import { useServerInsertedHTML } from 'next/navigation'
import { PropsWithChildren, useMemo } from 'react'
import { themeConfig } from '../../config/theme-config'
import '../../utils/initialize'

const AntdProvider = (props: PropsWithChildren) => {
  const cache = useMemo<Entity>(() => createCache(), [])
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
      <ConfigProvider theme={themeConfig}>{props.children}</ConfigProvider>
    </StyleProvider>
  )
}

export default AntdProvider
