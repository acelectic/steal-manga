'use client'

import { Col, Collapse, CollapseProps, Row, Tag, Typography } from 'antd'
import dayjs from 'dayjs'
import { useRouter } from 'next/navigation'
import { useMemo } from 'react'
import { IGetMangaUpdatedResponse } from '../../service/manga-updated/types'
import { AddMangaConfig } from './AddMangaConfig'
import { ConsoleAction } from './ConsoleAction'
import { DrivePortal } from './DrivePortal'
import { MangaTable } from './MangaTable'
import { MangaUpdateList } from './MangaUpdateList'

export interface IHomeProps {
  data?: IGetMangaUpdatedResponse
  authGoogleStatus?: boolean
}
export const Home = (props: IHomeProps) => {
  const { data, authGoogleStatus } = props
  const router = useRouter()
  const {
    updated,
    manMirrorCartoons = [],
    myNovelCartoons = [],
    resultsViewedSorted = [],
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
        <DrivePortal />
      </Col>
      <Col span={24}>
        <AddMangaConfig />
      </Col>
      <Col span={24}>
        <Collapse accordion items={items} />
      </Col>
      <MangaUpdateList
        resultsViewedSorted={resultsViewedSorted}
        resultsYetViewSorted={resultsYetViewSorted}
      />
    </Row>
  )
}
