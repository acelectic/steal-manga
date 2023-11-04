'use client'

import { Col, Collapse, CollapseProps, ConfigProvider, Row, Tag, Typography } from 'antd'
import dayjs from 'dayjs'
import { useRouter } from 'next/navigation'
import { useMemo } from 'react'
import { themeConfig } from '../../config/theme-config'
import { EnumMangaProjectName, IGetMangaUpdatedResponse } from '../../service/manga-updated/types'
import { IMangaUpload } from '../../utils/db-client/collection-interface'
import { AddMangaConfig } from './AddMangaConfig'
import { ConsoleAction } from './ConsoleAction'
import { DrivePortal } from './DrivePortal'
import { MangaTable } from './MangaTable'
import { MangaUpdateList } from './MangaUpdateList'

export interface IHomeProps {
  data?: IGetMangaUpdatedResponse
  mangaUploads?: IMangaUpload[]
  authGoogleStatus?: boolean
}
export const Home = (props: IHomeProps) => {
  const { data, authGoogleStatus, mangaUploads = [] } = props
  const router = useRouter()
  const { updated, manMirrorCartoons = [], myNovelCartoons = [] } = data || {}

  const items: CollapseProps['items'] = useMemo(() => {
    return [
      {
        key: 'man-mirror',
        label: 'Man Mirror',
        children: (
          <MangaTable title={EnumMangaProjectName.MAN_MIRROR} data={manMirrorCartoons} noHeader />
        ),
      },
      {
        key: 'my-novel',
        label: 'My Novel',
        children: (
          <MangaTable title={EnumMangaProjectName.MY_NOVEL} data={myNovelCartoons} noHeader />
        ),
      },
    ]
  }, [manMirrorCartoons, myNovelCartoons])

  return (
    <ConfigProvider theme={themeConfig}>
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
            <Col
              flex={1}
              sm={{
                span: 24,
              }}
            >
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
        <MangaUpdateList mangaUploads={mangaUploads} />
      </Row>
    </ConfigProvider>
  )
}
