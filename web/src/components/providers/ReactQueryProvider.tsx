'use client'

import { QueryClient, QueryClientConfig, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import React, { PropsWithChildren } from 'react'
//import queryClient from "../store";

interface IReactQueryProvider {
  options?: QueryClientConfig
}
const ReactQueryProvider = (props: PropsWithChildren<IReactQueryProvider>) => {
  const [queryClient] = React.useState(() => new QueryClient(props.options))
  return (
    <QueryClientProvider client={queryClient}>
      {props.children}
      {process.env.NEXT_PUBLIC_APP_MODE === 'development' && <ReactQueryDevtools />}
    </QueryClientProvider>
  )
}

export default ReactQueryProvider
