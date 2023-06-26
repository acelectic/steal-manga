'use client'

import styled from '@emotion/styled'
import { Col, Grid, Row, Tag } from 'antd'

const Layout = styled.div`
  position: fixed;
  bottom: 15px;
  right: 15px;

  pointer-events: none;
`
export const ScreenSizeIndicator = () => {
  const { xs, sm, md, lg, xl, xxl } = Grid.useBreakpoint()
  return (
    <Layout>
      <Row gutter={6} wrap={false}>
        {xs && (
          <Col>
            <Tag color="purple">xs</Tag>
          </Col>
        )}
        {sm && (
          <Col>
            <Tag color="purple">sm</Tag>
          </Col>
        )}
        {md && (
          <Col>
            <Tag color="purple">md</Tag>
          </Col>
        )}
        {lg && (
          <Col>
            <Tag color="purple">lg</Tag>
          </Col>
        )}
        {xl && (
          <Col>
            <Tag color="purple">xl</Tag>
          </Col>
        )}
        {xxl && (
          <Col>
            <Tag color="purple">xxl</Tag>
          </Col>
        )}
      </Row>
    </Layout>
  )
}
