'use client'

import React, { PropsWithChildren } from 'react'
import { Breadcrumb, Layout, Menu, theme } from 'antd'
import Navbar from './Navbar'
import { ScreenSizeIndicator } from './ScreenSizeIndicator'

const { Header, Content, Footer } = Layout

const AppLayout = (props: PropsWithChildren) => {
  const {
    token: { colorBgContainer },
  } = theme.useToken()

  return (
    <Layout className="layout">
      <Navbar />
      <Content style={{ padding: '0 50px' }}>
        {/* <Breadcrumb style={{ margin: '16px 0' }}>
          <Breadcrumb.Item>Home</Breadcrumb.Item>
          <Breadcrumb.Item>List</Breadcrumb.Item>
          <Breadcrumb.Item>App</Breadcrumb.Item>
        </Breadcrumb> */}
        <div className="site-layout-content" style={{ background: colorBgContainer }}>
          {props.children}
        </div>
        <ScreenSizeIndicator />
      </Content>
    </Layout>
  )
}

export default AppLayout
