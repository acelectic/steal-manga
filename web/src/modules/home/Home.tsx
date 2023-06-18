'use client'

import { Button, Col, Layout, Row, Tag, Typography } from 'antd'
import { IGetMangaUpdatedResponse } from '../../service/manga-updated/types'
import { MangaTable } from './MangaTable'
import { ConsoleAction } from './ConsoleAction'
import { join } from 'lodash'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

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

  return (
    <Row gutter={[16, 16]}>
      <Col span={24}>
        <Row gutter={[12, 12]} align="middle">
          <Col>
            <Typography>{updated}</Typography>
          </Col>
          <Col>
            <ConsoleAction />
          </Col>
          <Col>
            <Row gutter={8} align="middle">
              <Col>
                <Typography>Google Authen Status :</Typography>
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
        </Row>
      </Col>

      <Col span={24}>
        <MangaTable title="man-mirror" data={manMirrorCartoons} />
      </Col>
      <Col span={24}>
        <MangaTable title="my-novel" data={myNovelCartoons} />
      </Col>
      <Layout.Content style={{ backgroundColor: '#ffffff', borderRadius: '6px', padding: '20px' }}>
        <Row gutter={[18, 18]} style={{ width: '100%' }}>
          {resultsYetViewSorted.map(([updated, items = []]) => {
            return (
              <Col span={12} key={updated.toString()}>
                <Typography.Title level={5}>{updated.toString()}</Typography.Title>
                <ul style={{ marginLeft: 20 }}>
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
