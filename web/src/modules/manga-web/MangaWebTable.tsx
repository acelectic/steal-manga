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
} from 'antd'
import { ColumnType } from 'antd/es/table'
import { FilterConfirmProps, FilterDropdownProps } from 'antd/es/table/interface'
import axios from 'axios'
import { chain } from 'lodash'
import { useRouter } from 'next/navigation'
import React, { useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import Highlighter from 'react-highlight-words'
import { usePaginationHandle } from '../../utils/custom-hook'
import { IMangaWebData, IUpdateMangaWebPayload } from '../../utils/db-client/collection-interface'

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

type IItem = IMangaWebData

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

  // useEffect(() => {
  //   if (editable && dataType === 'boolean') {
  //     const formValues = form.getFieldsValue()
  //     const formValuesData = formValues?.[dataIndex]
  //     const data = record?.[dataIndex]
  //     console.log({ formValues, formValuesData, record, data })
  //     if (formValuesData === undefined && record && data !== undefined) {
  //       console.log({ dataIndex, formValuesData, record, data })
  //       form.setFieldsValue({ [dataIndex]: data })
  //     }
  //   }
  // }, [dataIndex, dataType, editable, form, record])

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
              <Input
                ref={inputRef}
                onPressEnter={save}
                onBlur={save}
                placeholder={typeof title === 'string' ? title : 'fill here'}
              />
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

interface IMangaWebTableProps {
  data: IMangaWebData[]
}

export const MangaWebTable = (props: IMangaWebTableProps) => {
  const { data } = props
  const paginateHandle = usePaginationHandle({
    prefix: 'manga-web',
    defaultPageSize: 5,
  })
  const [dataSource, setDataSource] = useState<IItem[]>([])
  const router = useRouter()

  const [searchText, setSearchText] = useState('')
  const [searchedColumn, setSearchedColumn] = useState<DataIndex>('')
  const searchInput = useRef<InputRef>(null)
  const { xs, sm } = Grid.useBreakpoint()

  const { mutate: saveMangaWeb } = useMutation(
    async (payload: IUpdateMangaWebPayload) => {
      const { data } = await axios.post('api/v1/manga-webs', {
        data: payload,
      })

      return data
    },
    {
      onError() {
        message.error('Save Failed')
      },
      onSettled() {
        router.refresh()

        setTimeout(() => {
          router.refresh()
        }, 500)
      },
    },
  )

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
        id: e.id,
        name: e.name,
        link: e.link,
      }),
    )
    setDataSource(chain(_data).orderBy(['name'], ['asc']).value())
  }, [data])

  const getFilterDropdown = useCallback(
    (dataIndex: DataIndex) => {
      const renderFilterDropdown = ({
        setSelectedKeys,
        selectedKeys,
        confirm,
        clearFilters,
        close,
      }: FilterDropdownProps) => (
        <div style={{ padding: 8 }} onKeyDown={(e) => e.stopPropagation()}>
          <Input
            ref={searchInput}
            placeholder={`Search ${dataIndex}`}
            value={selectedKeys[0]?.toString()}
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
      )
      return renderFilterDropdown
    },
    [handleReset, handleSearch],
  )

  const getFilterIcon = useCallback(():
    | React.ReactNode
    | ((filtered: boolean) => React.ReactNode) => {
    const renderFilterIcon = (filtered: boolean) => (
      <SearchOutlined style={{ color: filtered ? '#1677ff' : undefined }} />
    )
    return renderFilterIcon
  }, [])

  const getColumnSearchProps = useCallback(
    (dataIndex: DataIndex): ColumnType<IItem> => ({
      filterDropdown: getFilterDropdown(dataIndex),
      filterIcon: getFilterIcon(),
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
    [getFilterDropdown, getFilterIcon, searchText, searchedColumn],
  )

  const defaultColumns = useMemo(() => {
    const columns: (ColumnType<IItem> &
      Partial<Pick<EditableCellProps, 'editable' | 'dataType'>>)[] = [
      {
        title: 'Name',
        key: 'name',
        dataIndex: 'name',
        width: 250,
        editable: true,
        sorter: (a, b) => {
          if (a.name.toLowerCase() < b.name.toLowerCase()) return -1
          if (a.name.toLowerCase() > b.name.toLowerCase()) return 1
          return 0
        },
        ...getColumnSearchProps('name'),
      },
      {
        title: 'Url',
        key: 'link',
        dataIndex: 'link',
        editable: true,
        render: (value) => {
          return (
            <Typography.Paragraph style={{ margin: 0 }} copyable>
              {value}
            </Typography.Paragraph>
          )
        },
      },
    ]

    columns.push({
      title: 'Action',
      key: 'name',
      width: 150,
      render(value, record, index) {
        return (
          <Row gutter={[8, 8]} wrap={false}>
            <Col>
              <Button
                size="small"
                onClick={() => {
                  saveMangaWeb({
                    mangaWebs: [
                      {
                        id: record.id,
                        name: record.name,
                        link: record.link,
                      },
                    ],
                  })
                }}
              >
                Save
              </Button>
            </Col>
            {!!record.link && (
              <Col>
                <Button size="small" type="link" href={record.link}>
                  open
                </Button>
              </Col>
            )}
          </Row>
        )
      },
    })
    return columns
  }, [getColumnSearchProps, saveMangaWeb])

  const handleSave = (row: IItem) => {
    const newData = [...dataSource]
    const index = newData.findIndex((item) => row.id === item.id)
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
      <Table
        dataSource={dataSource}
        columns={columns as ColumnType<IItem>[]}
        rowKey={'id'}
        pagination={{
          current: paginateHandle.current,
          pageSize: paginateHandle.pageSize,
          onChange: paginateHandle.onChange,
          showSizeChanger: true,
          pageSizeOptions: paginateHandle.pageSizeOptions,
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
