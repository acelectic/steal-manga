import { Col, Layout, Row, Typography } from 'antd'
import { IGetMangaUpdatedResponse } from '../../service/manga-updated/types'
import { join } from 'lodash'

interface IMangeUpdateListProps {
  data: IGetMangaUpdatedResponse['resultsYetViewSorted']
}

export const MangeUpdateList = (props: IMangeUpdateListProps) => {
  const { data = [] } = props

  return (
    <Layout.Content style={{ backgroundColor: '#ffffff', borderRadius: '6px', padding: '20px' }}>
      <Row gutter={[18, 18]} style={{ width: '100%' }}>
        {data.map(([updated, items = []]) => {
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
  )
}
