'use client'
import { Button } from 'antd'
import { Content } from 'antd/es/layout/layout'

interface IAuthGoogleProps {
  authorizationUrl?: string
}

export const AuthGoogle = (props: IAuthGoogleProps) => {
  return (
    <Content style={{ padding: 50 }}>
      <Button
        type="primary"
        href={props.authorizationUrl}
        target="_self"
        disabled={!props.authorizationUrl}
      >
        Authen Google
      </Button>
    </Content>
  )
}
