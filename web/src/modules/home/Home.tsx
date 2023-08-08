'use client'

import { Col, Collapse, CollapseProps, Layout, Row, Tag, Typography } from 'antd'
import { IGetMangaUpdatedResponse } from '../../service/manga-updated/types'
import { MangaTable } from './MangaTable'
import { ConsoleAction } from './ConsoleAction'
import { join } from 'lodash'
import { useRouter } from 'next/navigation'
import { css } from '@emotion/css'
import { useMemo } from 'react'
import dayjs from 'dayjs'

const layoutCss = css`
  border: 1px solid black;
  border-radius: 6px;
  padding: 10px;
  margin: 0 20px;
`

export interface IHomeProps {
  data?: IGetMangaUpdatedResponse
  authGoogleStatus?: boolean
}
export const Home = (props: IHomeProps) => {
  const { data, authGoogleStatus } = props
  const router = useRouter()
  const {
    updated,
    // mangaExists,
    manMirrorCartoons = [],
    myNovelCartoons = [],
    resultsYetViewSorted = [],
  } = data || {}

  const items: CollapseProps['items'] = useMemo(() => {
    return [
      {
        key: 'man-mirror',
        label: 'Man Mirror',
        children: <MangaTable title="man-mirror" data={manMirrorCartoons} noHeader />,
      },
      {
        key: 'my-novel',
        label: 'My Novel',
        children: <MangaTable title="my-novel" data={myNovelCartoons} noHeader />,
      },
    ]
  }, [manMirrorCartoons, myNovelCartoons])

  return (
    <Row gutter={[16, 16]}>
      <Col span={24}>
        <Row gutter={[24, 24]} align="middle">
          <Col flex="none">
            <Row gutter={[8, 8]} align="middle">
              <Col span={24}>
                <Typography.Text>{dayjs(updated).tz().format()}</Typography.Text>
              </Col>
              <Col>
                <Typography.Text>Google Authen Status :</Typography.Text>
              </Col>
              <Col>
                <div
                  style={{ cursor: authGoogleStatus ? 'default' : 'pointer' }}
                  onClick={authGoogleStatus ? undefined : router.push.bind(null, '/auth/google')}
                >
                  <Tag color={authGoogleStatus ? 'green' : 'warning'}>
                    {authGoogleStatus ? 'Valid' : 'Invalid'}
                  </Tag>
                </div>
              </Col>
            </Row>
          </Col>
          <Col flex={1}>
            <ConsoleAction />
          </Col>
        </Row>
      </Col>

      <Col span={24}>
        <Collapse accordion items={items} />
      </Col>
      <Layout.Content style={{ backgroundColor: '#ffffff', borderRadius: '6px', padding: '20px' }}>
        <Row gutter={[18, 18]} style={{ width: '100%' }}>
          {resultsYetViewSorted.map(([updated, items = []]) => {
            return (
              <Col sm={8} xs={12} md={4.8} key={updated.toString()}>
                <Typography.Title level={5}>{updated.toString()}</Typography.Title>
                <ul style={{ marginLeft: 20, maxHeight: 300, overflowY: 'auto' }}>
                  {items.map((item) => {
                    return (
                      <li key={item.project + item.manga + item.chapter}>
                        <Typography>{join([item.manga, item.chapter], ' ')}</Typography>
                      </li>
                    )
                  })}
                </ul>
              </Col>
            )
          })}
        </Row>
      </Layout.Content>
    </Row>
  )
}
