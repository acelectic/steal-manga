'use client'

import { StyleProvider, createCache, extractStyle } from '@ant-design/cssinjs'
import type Entity from '@ant-design/cssinjs/es/Cache'
import { useServerInsertedHTML } from 'next/navigation'
import { PropsWithChildren, useMemo } from 'react'
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

  return <StyleProvider cache={cache}>{props.children}</StyleProvider>
}

export default AntdProvider
