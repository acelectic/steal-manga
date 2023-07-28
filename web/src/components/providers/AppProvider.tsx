import React from 'react'
import { PropsWithChildren } from 'react'
import ReactQueryProvider from './ReactQueryProvider'
import AntdProvider from './AntdProvider'
import EmotionProvider from './EmotionProvider'

export const AppProvider = (props: PropsWithChildren) => {
  return (
    <ReactQueryProvider>
      <AntdProvider>
        <EmotionProvider>{props.children}</EmotionProvider>
      </AntdProvider>
    </ReactQueryProvider>
  )
}
