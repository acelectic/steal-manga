import { Col, Divider, Layout, Row, Typography } from 'antd'
import { IGetMangaUpdatedResponse } from '../../service/manga-updated/types'
import { join } from 'lodash'
import { useCallback } from 'react'

interface IMangeUpdateListProps {
  resultsYetViewSorted: IGetMangaUpdatedResponse['resultsYetViewSorted']
  resultsViewedSorted: IGetMangaUpdatedResponse['resultsViewedSorted']
}

export const MangeUpdateList = (props: IMangeUpdateListProps) => {
  const { resultsViewedSorted = [], resultsYetViewSorted = [] } = props

  const renderData = useCallback((d: IGetMangaUpdatedResponse['resultsYetViewSorted']) => {
    return d.map(([updated, items = []]) => {
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
    })
  }, [])

  return (
    <Layout.Content style={{ backgroundColor: '#ffffff', borderRadius: '6px', padding: '20px' }}>
      <Row gutter={[18, 18]} style={{ width: '100%' }}>
        {renderData(resultsYetViewSorted)}
      </Row>
      <Divider type="horizontal" orientationMargin="8px" />
      <Row gutter={[18, 18]} style={{ width: '100%' }}>
        {renderData(resultsViewedSorted)}
      </Row>
    </Layout.Content>
  )
}
