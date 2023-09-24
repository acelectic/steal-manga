'use client'
import { SearchOutlined } from '@ant-design/icons'
import { css } from '@emotion/css'
import { useMutation } from '@tanstack/react-query'
import {
  Button,
  Col,
  Form,
  FormInstance,
  Grid,
  Input,
  InputRef,
  Row,
  Space,
  Switch,
  Table,
  Typography,
  message,
  theme,
} from 'antd'
import { ColumnType } from 'antd/es/table'
import { FilterConfirmProps } from 'antd/es/table/interface'
import { chain } from 'lodash'
import React, { useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import Highlighter from 'react-highlight-words'
import { updateMangaConfig } from '../../service/manga-updated'
import { IGetMangaUpdatedResponse, ManMirrorCartoon } from '../../service/manga-updated/types'
import { triggerDownloadMangaOne } from '../../service/trigger-download'
import { usePaginationHandle } from '../../utils/custom-hook'
import { openGoogleDrive } from '../../utils/helper'

const warpCss = css`
  width: 100%;

  .editable-cell {
    position: relative;
  }

  .editable-cell-value-wrap {
    padding: 5px 12px;
    cursor: pointer;
    min-height: 32px;
  }

  .editable-cell-value-wrap:hover {
    padding: 4px 11px;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
  }
`

const EditableContext = React.createContext<FormInstance<any> | null>(null)

type IItem = ManMirrorCartoon

type DataIndex = keyof IItem

interface IEditableRowProps {
  index: number
}
const EditableRow: React.FC<IEditableRowProps> = ({ index, ...props }) => {
  const [form] = Form.useForm()
  return (
    <Form form={form} component={false} /*  initialValues={initialValues} */>
      <EditableContext.Provider value={form}>
        <tr {...props} />
      </EditableContext.Provider>
    </Form>
  )
}

interface EditableCellProps {
  title: React.ReactNode
  editable: boolean
  dataType: 'number' | 'string' | 'boolean'
  children: React.ReactNode
  dataIndex: keyof IItem
  record: IItem
  handleSave: (record: IItem) => void
}

const EditableCell: React.FC<EditableCellProps> = ({
  title,
  editable,
  children,
  dataIndex,
  dataType,
  record,
  handleSave,
  ...restProps
}) => {
  const [editing, setEditing] = useState(false)
  const inputRef = useRef<InputRef>(null)
  const form = useContext(EditableContext)!

  useEffect(() => {
    if (editing) {
      inputRef.current?.focus?.()
    }
  }, [editing])

  const toggleEdit = () => {
    setEditing(!editing)
    form.setFieldsValue({ [dataIndex]: record[dataIndex] })
  }

  const save = async () => {
    try {
      const values = await form.validateFields()
      toggleEdit()
      handleSave({ ...record, ...values })
    } catch (errInfo) {
      console.log('Save failed:', errInfo)
    }
  }

  let childNode = children

  const renderChildren = useMemo(() => {
    return children
  }, [children])

  if (editable) {
    childNode = editing ? (
      <Row gutter={12} align="middle">
        <Col>
          <Form.Item
            style={{ margin: 0 }}
            name={dataIndex}
            rules={[
              {
                required: true,
                message: `${title} is required.`,
              },
            ]}
            valuePropName={dataType === 'boolean' ? 'checked' : undefined}
          >
            {dataType === 'boolean' ? (
              <Switch />
            ) : (
              <Input ref={inputRef} onPressEnter={save} onBlur={save} />
            )}
          </Form.Item>
        </Col>
        {dataType === 'boolean' && (
          <Col>
            <Button onClick={save} size="small">
              Save
            </Button>
          </Col>
        )}
      </Row>
    ) : (
      <div className="editable-cell-value-wrap" style={{ paddingRight: 24 }} onClick={toggleEdit}>
        {renderChildren}
      </div>
    )
  }

  return <td {...restProps}>{childNode}</td>
}

interface IMangaTableProps {
  title: 'man-mirror' | 'my-novel'
  data: IGetMangaUpdatedResponse['manMirrorCartoons'] | IGetMangaUpdatedResponse['myNovelCartoons']
  noHeader?: true
}
export const MangaTable = (props: IMangaTableProps) => {
  const { title, data, noHeader = false } = props
  const paginateHandle = usePaginationHandle({
    prefix: title,
  })
  const [dataSource, setDataSource] = useState<IItem[]>([])

  const [searchText, setSearchText] = useState('')
  const [searchedColumn, setSearchedColumn] = useState('')
  const searchInput = useRef<InputRef>(null)
  const { colorBgMask, colorSuccessActive } = theme.getDesignToken()
  const { xs, sm } = Grid.useBreakpoint()

  const {
    mutate: updateConfig,
    variables: updateConfigParams,
    isLoading: isUpdateConfigLoading,
  } = useMutation(updateMangaConfig, {
    onSuccess: () => {
      message.success('Update Config Success')
    },
  })

  const {
    mutate: downloadMangaOne,
    variables: downloadOneParams,
    isLoading: isDownloadMangaOneLoading,
  } = useMutation(triggerDownloadMangaOne, {
    onSuccess: () => {
      message.success('Download Success')
    },
  })

  const handleSearch = useCallback(
    (
      selectedKeys: string[],
      confirm: (param?: FilterConfirmProps) => void,
      dataIndex: DataIndex,
    ) => {
      confirm()
      setSearchText(selectedKeys[0])
      setSearchedColumn(dataIndex)
    },
    [],
  )

  const handleReset = useCallback((clearFilters: () => void) => {
    clearFilters()
    setSearchText('')
  }, [])

  useEffect(() => {
    const _data = data.map(
      (e): IItem => ({
        cartoonName: e.cartoonName,
        cartoonId: e.cartoonId,
        latestChapter: +e.latestChapter,
        maxChapter: +e.maxChapter,
        disabled: !!e.disabled,
        downloaded: +e.downloaded,
        cartoonDriveId: e.cartoonDriveId,
        projectName: e.projectName,
      }),
    )
    setDataSource(chain(_data).orderBy(['cartoonName'], ['asc']).value())
  }, [data])

  const getColumnSearchProps = useCallback(
    (dataIndex: DataIndex): ColumnType<IItem> => ({
      filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters, close }) => (
        <div style={{ padding: 8 }} onKeyDown={(e) => e.stopPropagation()}>
          <Input
            ref={searchInput}
            placeholder={`Search ${dataIndex}`}
            value={selectedKeys[0]}
            onChange={(e) => setSelectedKeys(e.target.value ? [e.target.value] : [])}
            onPressEnter={() => handleSearch(selectedKeys as string[], confirm, dataIndex)}
            style={{ marginBottom: 8, display: 'block' }}
          />
          <Space>
            <Button
              type="primary"
              onClick={() => handleSearch(selectedKeys as string[], confirm, dataIndex)}
              icon={<SearchOutlined />}
              size="small"
              style={{ width: 90 }}
            >
              Search
            </Button>
            <Button
              onClick={() => clearFilters && handleReset(clearFilters)}
              size="small"
              style={{ width: 90 }}
            >
              Reset
            </Button>
            <Button
              type="link"
              size="small"
              onClick={() => {
                confirm({ closeDropdown: false })
                setSearchText((selectedKeys as string[])[0])
                setSearchedColumn(dataIndex)
              }}
            >
              Filter
            </Button>
            <Button
              type="link"
              size="small"
              onClick={() => {
                close()
              }}
            >
              close
            </Button>
          </Space>
        </div>
      ),
      filterIcon: (filtered: boolean) => (
        <SearchOutlined style={{ color: filtered ? '#1677ff' : undefined }} />
      ),
      onFilter: (value, record) =>
        record[dataIndex]
          .toString()
          .toLowerCase()
          .includes((value as string).toLowerCase()),
      onFilterDropdownOpenChange: (visible) => {
        if (visible) {
          setTimeout(() => searchInput.current?.select(), 100)
        }
      },
      render: (text) =>
        searchedColumn === dataIndex ? (
          <Highlighter
            highlightStyle={{ backgroundColor: '#ffc069', padding: 0 }}
            searchWords={[searchText]}
            autoEscape
            textToHighlight={text ? text.toString() : ''}
          />
        ) : (
          text
        ),
    }),
    [handleReset, handleSearch, searchText, searchedColumn],
  )

  const defaultColumns = useMemo(() => {
    const columns: (ColumnType<IItem> &
      Partial<Pick<EditableCellProps, 'editable' | 'dataType'>>)[] = [
      {
        title: 'Cartoon Name',
        key: 'cartoonName',
        dataIndex: 'cartoonName',
        width: 400,
        sorter: (a, b) => {
          if (a.cartoonName.toLowerCase() < b.cartoonName.toLowerCase()) return -1
          if (a.cartoonName.toLowerCase() > b.cartoonName.toLowerCase()) return 1
          return 0
        },
        ...getColumnSearchProps('cartoonName'),
      },
      {
        title: 'Cartoon Id',
        key: 'cartoonId',
        dataIndex: 'cartoonId',
        width: 250,
        render: (value) => {
          return <Typography.Paragraph copyable>{value}</Typography.Paragraph>
        },
      },
      {
        title: 'Latest Chapter',
        key: 'latestChapter',
        dataIndex: 'latestChapter',
        editable: title === 'my-novel',
      },
    ]

    if (title === 'man-mirror') {
      columns.push({
        title: 'Max Chapter',
        key: 'maxChapter',
        dataIndex: 'maxChapter',
        editable: title === 'man-mirror',
      })
    }
    columns.push({
      title: 'Disabled',
      key: 'disabled',
      dataIndex: 'disabled',
      editable: true,
      dataType: 'boolean',
      render: (value: boolean) => (
        <Typography.Text
          color={!!value ? colorSuccessActive : colorBgMask}
          style={{ fontWeight: 'bold' }}
        >
          {!!value ? 'True' : 'False'}
        </Typography.Text>
      ),
    })
    columns.push({ title: 'Downloaded', key: 'downloaded', dataIndex: 'downloaded' })
    columns.push({
      title: 'Action',
      key: 'cartoonId',
      render(value, record, index) {
        return (
          <Row gutter={[8, 8]} wrap={false}>
            <Col>
              <Button
                size="small"
                onClick={() => {
                  updateConfig({
                    projectName: title,
                    cartoonId: record.cartoonId,
                    cartoonName: record.cartoonName,
                    latestChapter: +record.latestChapter,
                    maxChapter: +record.maxChapter,
                    disabled: record.disabled,
                    downloaded: record.downloaded,
                  })
                }}
                loading={
                  isUpdateConfigLoading && updateConfigParams?.cartoonId === record.cartoonId
                }
                disabled={isUpdateConfigLoading || isDownloadMangaOneLoading}
              >
                Save
              </Button>
            </Col>
            <Col>
              <Button
                size="small"
                type="primary"
                onClick={async () => {
                  await downloadMangaOne({
                    projectName: title,
                    cartoonId: record.cartoonId,
                    cartoonName: record.cartoonName,
                    latestChapter: +record.latestChapter,
                    maxChapter: +record.maxChapter,
                    disabled: record.disabled,
                    downloaded: record.downloaded,
                  })
                }}
                loading={
                  isDownloadMangaOneLoading && downloadOneParams?.cartoonId === record.cartoonId
                }
                disabled={isUpdateConfigLoading || isDownloadMangaOneLoading}
              >
                Download
              </Button>
            </Col>
            {!!record.cartoonDriveId && (
              <Col>
                <Button
                  size="small"
                  type="link"
                  onClick={openGoogleDrive.bind(null, record.cartoonDriveId)}
                >
                  Drive
                </Button>
              </Col>
            )}
          </Row>
        )
      },
    })
    return columns
  }, [
    colorBgMask,
    colorSuccessActive,
    downloadMangaOne,
    downloadOneParams?.cartoonId,
    getColumnSearchProps,
    isDownloadMangaOneLoading,
    isUpdateConfigLoading,
    title,
    updateConfig,
    updateConfigParams?.cartoonId,
  ])

  const handleSave = (row: IItem) => {
    const newData = [...dataSource]
    const index = newData.findIndex((item) => row.cartoonId === item.cartoonId)
    const item = newData[index]
    newData.splice(index, 1, {
      ...item,
      ...row,
    })
    setDataSource(newData)
  }

  const columns = defaultColumns.map((col) => {
    if (!col.editable) {
      return col
    }
    return {
      ...col,
      width: '200px',
      onCell: (record: IItem) => ({
        record,
        editable: col.editable,
        dataIndex: col.dataIndex,
        title: col.title,
        dataType: col.dataType,
        handleSave,
      }),
    }
  })

  return (
    <Space className={warpCss} direction="vertical" size={8}>
      {!noHeader && <Typography.Title level={3}>{title}</Typography.Title>}
      <Table
        dataSource={dataSource}
        columns={columns as ColumnType<IItem>[]}
        rowKey={'cartoonId'}
        pagination={{
          pageSizeOptions: [5, 10, 20, 30, 50],
          showSizeChanger: true,
          current: paginateHandle.current,
          pageSize: paginateHandle.pageSize,
          onChange: paginateHandle.onChange,
        }}
        components={{
          body: {
            row: EditableRow,
            cell: EditableCell,
          },
        }}
        scroll={{
          x: sm || xs ? 500 : undefined,
        }}
        size="small"
        showSorterTooltip
        bordered
      />
    </Space>
  )
}
