'use client'

import { Col, Collapse, Layout, Row, Typography } from 'antd'
import { IGetMangaUpdatedResponse } from '../../service/manga-updated/types'
import { MangaTable } from './MangaTable'
import { ConsoleAction } from './ConsoleAction'
import { AppProvider } from '../../components/providers/AppProvider'
import dayjs from 'dayjs'
import { join } from 'lodash'

export interface IHomeProps {
  data?: IGetMangaUpdatedResponse
}
export const Home = (props: IHomeProps) => {
  const { data } = props

  const {
    updated,
    mangaExists,
    manMirrorCartoons = [],
    myNovelCartoons = [],
    resultsYetViewSorted = [],
  } = data || {}

  return (
    <AppProvider>
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Row gutter={[12, 12]} align="middle">
            <Col>
              <Typography>{updated}</Typography>
            </Col>
            <Col>
              <ConsoleAction />
            </Col>
          </Row>
        </Col>

        <Col span={24}>
          <MangaTable title="man-mirror" data={manMirrorCartoons} />
        </Col>
        <Col span={24}>
          <MangaTable title="my-novel" data={myNovelCartoons} />
        </Col>
        <Layout.Content
          style={{ backgroundColor: '#ffffff', borderRadius: '6px', padding: '20px' }}
        >
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
    </AppProvider>
  )
}
