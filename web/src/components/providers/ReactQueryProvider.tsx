'use client'

import { QueryClient, QueryClientConfig, QueryClientProvider } from '@tanstack/react-query'
import React, { PropsWithChildren } from 'react'
//import queryClient from "../store";

interface IReactQueryProvider {
  options?: QueryClientConfig
}
const ReactQueryProvider = (props: PropsWithChildren<IReactQueryProvider>) => {
  const [queryClient] = React.useState(() => new QueryClient(props.options))
  return <QueryClientProvider client={queryClient}>{props.children}</QueryClientProvider>
}

export default ReactQueryProvider
