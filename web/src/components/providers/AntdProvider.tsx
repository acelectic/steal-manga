'use client'

import React, { useState } from 'react'
import { PropsWithChildren } from 'react'
import { StyleProvider, createCache, extractStyle } from '@ant-design/cssinjs'
import { useServerInsertedHTML } from 'next/navigation'

const AntdProvider = (props: PropsWithChildren) => {
  const [cache] = useState(() => createCache())
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
