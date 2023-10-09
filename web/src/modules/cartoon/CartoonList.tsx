'use client'

import { CheckOutlined, WarningOutlined } from '@ant-design/icons'
import { Col, Row, Table, Typography, theme } from 'antd'
import { ColumnType } from 'antd/es/table'
import { chain } from 'lodash'
import { useMemo } from 'react'
import { usePaginationOptions } from '../../utils/custom-hook'
import { IMangaUpload } from '../../utils/db-client/collection-interface'

interface ICartoonListProps {
  cartoonId: string
  projectName: string
  cartoonName: string
  data: IMangaUpload[]
}
export const CartoonList = (props: ICartoonListProps) => {
  const { cartoonId, cartoonName, projectName, data } = props
  const paginationOptions = usePaginationOptions()
  const { token } = theme.useToken()

  const columns = useMemo((): ColumnType<IMangaUpload>[] => {
    return [
      {
        title: '#',
        dataIndex: 'manga_chapter_name',
        width: 60,
        sorter: true,
        render: (value, record, index) => {
          return index + 1
        },
      },

      {
        title: 'ChapterName',
        dataIndex: 'manga_chapter_name',
      },
      {
        title: 'ChapterName',
        dataIndex: 'manga_chapter_name',
        render: (value: string) => {
          return value
            .match(/^[\d]+\.pdf/)
            ?.toString()
            ?.replace('.pdf', '')
        },
      },
      {
        title: 'DriveId',
        dataIndex: 'manga_chapter_drive_id',
      },
      {
        title: 'CreatedTime',
        dataIndex: 'created_time',
      },
      {
        title: 'modifiedByMeTime',
        dataIndex: 'modified_by_me_time',
      },
      {
        title: 'ViewedByMe',
        dataIndex: 'viewed_by_me',
        filters: [
          {
            text: 'Viewed',
            value: true,
          },
          {
            text: 'Yet View',
            value: false,
          },
        ],
        onFilter: (value, record) => (value === true ? record.viewed_by_me === true : false),
        render: (value: boolean) => {
          return value === true ? (
            <CheckOutlined
              style={{
                color: token.colorSuccessActive,
              }}
            />
          ) : (
            <WarningOutlined
              style={{
                color: token.colorWarning,
              }}
            />
          )
        },
      },
    ]
  }, [token.colorSuccessActive, token.colorWarning])

  const dataSource = useMemo(() => {
    return chain(data)
      .orderBy(
        [
          (d) => {
            return Number(
              d.manga_chapter_name
                .match(/^[\d]+\.pdf/)
                ?.toString()
                ?.replace('.pdf', ''),
            )
          },
        ],
        ['desc'],
      )
      .defaultTo([])
      .value()
  }, [data])
  return (
    <Row
      gutter={[16, 16]}
      style={{
        padding: 20,
      }}
    >
      <Col span={24}>
        <Row gutter={[8, 8]} align="middle">
          <Col>
            <Typography.Title level={3}>{projectName}</Typography.Title>
          </Col>
          <Col>
            <Typography.Title level={5}>{cartoonName}</Typography.Title>
          </Col>
        </Row>
      </Col>
      <Col span={24}>
        <Table
          rowKey="manga_chapter_name"
          size="small"
          columns={columns}
          dataSource={dataSource}
          pagination={paginationOptions}
          scroll={{ y: 400 }}
          sticky
          bordered
        />
      </Col>
    </Row>
  )
}
