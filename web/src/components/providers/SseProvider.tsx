'use client'
import React, { createContext, useMemo, useState } from 'react'

type ISseContextValue = Record<string, EventSource>

type ISseContextCustomFunction = {
  reset: () => void
  initialValues: ISseContextValue
}

type ISseContext = [
  state: ISseContextValue,
  setState: (v: ISseContextValue) => void,
  getEventSource: (url: string) => EventSource,
  removeEventSource: (url: string) => void,
  customFunction: ISseContextCustomFunction,
]

const sseContextDefaultValues: ISseContext = [
  {},
  () => {
    //
  },
  () => {
    return new EventSource('')
  },
  () => {
    //
  },
  {
    reset: () => {
      //
    },
    initialValues: {},
  },
]
export const SSEContext = createContext<ISseContext>(sseContextDefaultValues)

const SseProvider = ({ children }: { children: React.ReactNode }) => {
  const [state, setState] = useState<ISseContextValue>({})
  const value = useMemo((): ISseContext => {
    return [
      state,
      (v) => {
        setState(v)
      },
      (url) => {
        if (state[url]) {
          return state[url]
        } else {
          const eventSource = new EventSource(url)
          setState((prev) => {
            prev[url] = eventSource
            return prev
          })
          return eventSource
        }
      },
      (url) => {
        setState((prev) => {
          delete prev[url]
          return prev
        })
      },
      {
        initialValues: {},
        reset: () => {
          setState({})
        },
      },
    ]
  }, [state])

  return <SSEContext.Provider value={value}>{children}</SSEContext.Provider>
}

export default SseProvider
