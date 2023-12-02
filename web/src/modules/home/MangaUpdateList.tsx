import { css } from '@emotion/css'
import { Col, Layout, Row, Table, Tag, Typography } from 'antd'
import { ColumnsType, TableProps } from 'antd/es/table'
import dayjs from 'dayjs'
import { chain, join } from 'lodash'
import { useCallback, useMemo, useState } from 'react'
import { usePaginationOptions } from '../../utils/custom-hook'
import { IMangaUpload } from '../../utils/db-client/collection-interface'
import { makeGoogleDriveLink } from '../../utils/helper'

const linkCss = css`
  white-space: pre-line;
  text-align: start;
`
interface IMangaUpdateListProps {
  mangaUploads: IMangaUpload[]
}

type IItem = [string, IMangaUpload[]]

export const MangaUpdateList = (props: IMangaUpdateListProps) => {
  const { mangaUploads = [] } = props
  const [expandedRowKeys, setExpandedRowKeys] = useState<string[]>([])
  const paginationOptions = usePaginationOptions({
    prefix: 'manga-update-list',
    defaultPageSize: 5,
    paginationOptions: {
      pageSizeOptions: [5, 10, 20],
    },
  })
  const dataSource = useMemo(() => {
    return chain(mangaUploads)
      .groupBy((e) => dayjs.utc(e.created_time).local().format('YYYY/MM/DD'))
      .entries()
      .orderBy([([updated]) => dayjs(updated).toDate()], ['desc'])
      .value()
  }, [mangaUploads])

  const columns = useMemo((): ColumnsType<IItem> => {
    return [
      {
        title: 'Uploaded At',
        dataIndex: '0',
        key: '0',
        render: (value) => {
          const uploadedAt = dayjs(value, {
            format: 'YYYY/MM/DD',
          }).local()

          const isNew = uploadedAt.isSameOrAfter(
            dayjs().local().subtract(24, 'hour').startOf('hour'),
          )
          return (
            <Row gutter={8}>
              <Col>
                <Typography.Text>{uploadedAt.format('DD-MM-YYYY')}</Typography.Text>
              </Col>
              <Col>{isNew && <Tag color="success">New</Tag>}</Col>
            </Row>
          )
        },
      },
      Table.EXPAND_COLUMN,
    ]
  }, [])

  const expandedRowRender = useCallback<
    Exclude<Exclude<TableProps<IItem>['expandable'], undefined>['expandedRowRender'], undefined>
  >((record: IItem) => {
    const [, items] = record
    return (
      <ul style={{ marginLeft: 20, maxHeight: 200, overflowY: 'auto' }}>
        {chain(items)
          .orderBy(
            [
              (d) => d.cartoon_name,
              (d) =>
                Number(
                  d.manga_chapter_name
                    .match(/^[\d]+$/g)
                    ?.toString()
                    ?.replace('.pdf', ''),
                ),
            ],
            ['asc', 'asc'],
          )
          .map((item) => {
            return (
              <li key={item.project_name + item.cartoon_name + item.manga_chapter_name}>
                <Typography.Link
                  href={makeGoogleDriveLink(item.cartoon_drive_id)}
                  target="_blank"
                  className={linkCss}
                >
                  {join([item.cartoon_name, item.manga_chapter_name], ' ')}
                </Typography.Link>
              </li>
            )
          })
          .value()}
      </ul>
    )
  }, [])

  return (
    <Layout.Content style={{ backgroundColor: '#ffffff', borderRadius: '6px', padding: '20px' }}>
      <Table
        rowKey={([k]) => k}
        dataSource={dataSource}
        columns={columns}
        expandable={{
          expandRowByClick: true,
          expandedRowKeys,
          onExpand(expanded, record) {
            const [updated] = record
            if (expanded) setExpandedRowKeys([updated])
            else setExpandedRowKeys([])
          },
          expandedRowRender,
        }}
        pagination={paginationOptions}
      />
    </Layout.Content>
  )
}
