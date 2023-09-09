'use client'

import { useEffect } from 'react'
import LogRocket from 'logrocket'
import { appConfig } from '../../config/app-config'

export const InitLogRocker = (props: { NEXT_PUBLIC_LOG_ROCKET_APP_ID: string }) => {
  useEffect(() => {
    // console.log({ effect: appConfig })
    if (props?.NEXT_PUBLIC_LOG_ROCKET_APP_ID) {
      LogRocket.init(props.NEXT_PUBLIC_LOG_ROCKET_APP_ID || 'mlyfa/mini-bear')

      LogRocket.identify('Admin', {
        name: 'James Morrison',
        email: 'jamesmorrison@example.com',
        // Add your own custom user variables here, ie:
        subscriptionType: 'pro',
      })
    }
  }, [props.NEXT_PUBLIC_LOG_ROCKET_APP_ID])

  return <></>
}
