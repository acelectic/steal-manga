import { css } from '@emotion/css'
import { Col, Divider, Layout, Row, Typography } from 'antd'
import { chain, join } from 'lodash'
import { useCallback } from 'react'
import { IGetMangaUpdatedResponse } from '../../service/manga-updated/types'
import { makeGoogleDriveLink } from '../../utils/helper'

const linkCss = css`
  white-space: pre-line;
  text-align: start;
`
interface IMangaUpdateListProps {
  resultsYetViewSorted: IGetMangaUpdatedResponse['resultsYetViewSorted']
  resultsViewedSorted: IGetMangaUpdatedResponse['resultsViewedSorted']
}

export const MangaUpdateList = (props: IMangaUpdateListProps) => {
  const { resultsViewedSorted = [], resultsYetViewSorted = [] } = props

  const renderData = useCallback((d: IGetMangaUpdatedResponse['resultsYetViewSorted']) => {
    return d.map(([updated, items = []]) => {
      return (
        <Col sm={6} xs={12} md={4.8} key={updated.toString()}>
          <Typography.Title level={5}>{updated.toString()}</Typography.Title>
          <ul style={{ marginLeft: 20, maxHeight: 300, overflowY: 'auto' }}>
            {chain(items)
              .orderBy(['cartoonName', 'mangaChapterName'], ['asc', 'asc'])
              .map((item) => {
                return (
                  <li key={item.projectName + item.cartoonName + item.mangaChapterName}>
                    <Typography.Link
                      href={makeGoogleDriveLink(item.cartoonDriveId)}
                      target="_blank"
                      className={linkCss}
                    >
                      {join([item.cartoonName, item.mangaChapterName], ' ')}
                    </Typography.Link>
                  </li>
                )
              })
              .value()}
          </ul>
        </Col>
      )
    })
  }, [])

  return (
    <Layout.Content style={{ backgroundColor: '#ffffff', borderRadius: '6px', padding: '20px' }}>
      <Row
        gutter={[18, 18]}
        style={{
          width: '100%',
          padding: '10px',
          boxSizing: 'border-box',
          border: '1px solid black',
          borderRadius: '8px',
        }}
      >
        <Col span={24}>
          <Typography
            style={{
              color: '#25006b',
              fontWeight: 'bold',
            }}
          >
            ยังไม่อ่าน
          </Typography>
        </Col>
        {renderData(resultsYetViewSorted)}
      </Row>
      <Divider type="horizontal" orientationMargin="8px" />
      {/* <Row
        gutter={[18, 18]}
        style={{
          width: '100%',
          padding: '10px',
          boxSizing: 'border-box',
          border: '1px solid black',
          borderRadius: '8px',
        }}
      >
        <Col span={24}>
          <Typography
            style={{
              color: '#25006b',
              fontWeight: 'bold',
            }}
          >
            อ่านแล้ว
          </Typography>
        </Col>
        {renderData(resultsViewedSorted)}
      </Row> */}
    </Layout.Content>
  )
}
