'use client'
import { SearchOutlined } from '@ant-design/icons'
import { css } from '@emotion/css'
import { useMutation } from '@tanstack/react-query'
import {
  Button,
  Col,
  ConfigProvider,
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
import dayjs, { Dayjs } from 'dayjs'
import Gradient from 'javascript-color-gradient'
import { chain, round } from 'lodash'
import { useRouter } from 'next/navigation'
import React, { useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import Highlighter from 'react-highlight-words'
import { useInView } from 'react-intersection-observer'
import { themeConfig } from '../../config/theme-config'
import { updateMangaConfig } from '../../service/manga-updated'
import {
  EnumMangaProjectName,
  IGetMangaUpdatedResponse,
  ManMirrorCartoon,
} from '../../service/manga-updated/types'
import { triggerDownloadMangaOne } from '../../service/trigger-download'
import { usePaginationOptions, useSse } from '../../utils/custom-hook'
import { openGoogleDrive, openLink } from '../../utils/helper'

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

  tr.ant-table-row:hover {
    background-color: rgb(231, 231, 231);
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
  title: EnumMangaProjectName
  data: IGetMangaUpdatedResponse['manMirrorCartoons'] | IGetMangaUpdatedResponse['myNovelCartoons']
  noHeader?: true
}
export const MangaTable = (props: IMangaTableProps) => {
  const { title, data, noHeader = false } = props
  const paginateOptions = usePaginationOptions({
    prefix: title,
    paginationOptions: {
      showSizeChanger: true,
    },
  })
  const router = useRouter()
  const [dataSource, setDataSource] = useState<IItem[]>([])

  const [searchText, setSearchText] = useState('')
  const [searchedColumn, setSearchedColumn] = useState('')
  const searchInput = useRef<InputRef>(null)
  const { colorBgMask, colorSuccessActive } = theme.getDesignToken()
  const { xs, sm } = Grid.useBreakpoint()
  const { ref, inView } = useInView()
  const { data: cartoonDownloadingIdsData } = useSse<{
    cartoonDownloadingIds: string[]
  }>(`${process.env.NEXT_PUBLIC_API_HOST}/api/v1/manga-downloads/cartoons-status`, inView)
  const { cartoonDownloadingIds = [] } = cartoonDownloadingIdsData || {}

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
    setDataSource(chain(data).orderBy(['cartoonName'], ['asc']).value())
  }, [data])

  const getColumnSearchProps = useCallback(
    (dataIndex: DataIndex): ColumnType<IItem> => ({
      filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters, close }) => (
        <div style={{ padding: 8 }} onKeyDown={(e) => e.stopPropagation()}>
          <Input
            ref={searchInput}
            placeholder={`Search ${dataIndex}`}
            value={selectedKeys?.[0]?.toString()}
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
        !!record[dataIndex]
          ?.toString()
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

  const getLatestSyncColor = useCallback(
    (latestSync: Dayjs) => {
      const minColor = [255, 0, 0, 1]
      const maxColor = [0, 255, 21, 1]
      function pickHex(color1: number[], color2: number[], weight: number) {
        var p = weight
        var w = p * 2 - 1
        var w1 = (w / 1 + 1) / 2
        var w2 = 1 - w1
        var rgb = [
          Math.round(color1[0] * w1 + color2[0] * w2),
          Math.round(color1[1] * w1 + color2[1] * w2),
          Math.round(color1[2] * w1 + color2[2] * w2),
        ] as const
        return rgb
      }
      const dataChain = chain(dataSource).map((d) =>
        d.latestSync ? dayjs(d.latestSync).unix() : null,
      )
      const minLatestSync = dataChain.compact().min().value()
      const maxLatestSync = dataChain.compact().max().value()
      const weight = (dayjs(latestSync).unix() - minLatestSync) / (maxLatestSync - minLatestSync)
      const target = Math.min(round(weight * 255, 0), 255)
      const colorOpacity = target.toString(16)
      const colorHex = pickHex(minColor, maxColor, weight)
      const colorsSize = 20
      const color = new Gradient().setColorGradient('#E74B4B', '#3BEE4A').setMidpoint(colorsSize)

      const calIndex = colorsSize * weight
      const colorIndex = Math.min(Math.max(round(calIndex, 0), 1), colorsSize)
      const colors = color.getColors()
      const finalColor = color.getColor(colorIndex)
      console.log({
        minLatestSync,
        maxLatestSync,
        weight,
        target,
        colorOpacity,
        colorHex,
        colors,
        finalColor,
        colorIndex,
        calIndex,
      })
      return finalColor
      // return `rgba(${colorHex.concat([target]).join()})`
    },
    [dataSource],
  )

  const onCartoonIdClick = useCallback(
    (cartoonId: string) => {
      const myNovelLink = `https://mynovel.co/BookPreview?Pid=${cartoonId}`
      const manMirrorLink = `https://www.manmirror.net/readpost.php?postId=${cartoonId}`

      if (title === EnumMangaProjectName.MY_NOVEL) openLink(myNovelLink)
      if (title === EnumMangaProjectName.MAN_MIRROR) openLink(manMirrorLink)
    },
    [title],
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
        render: (value, record) => {
          return (
            <Typography.Link
              onClick={() => {
                router.push(`cartoons/${record.cartoonId}`)
              }}
            >
              {value}
            </Typography.Link>
          )
        },
      },
      {
        title: 'Cartoon Id',
        key: 'cartoonId',
        dataIndex: 'cartoonId',
        width: 250,
        render: (value) => {
          return (
            <Typography.Link
              onClick={onCartoonIdClick.bind(null, value)}
              copyable={{
                text: value,
              }}
            >
              {value}
            </Typography.Link>
          )
        },
      },
      {
        title: 'Latest Chapter',
        key: 'latestChapter',
        dataIndex: 'latestChapter',
        editable: true,
      },
      {
        title: 'Max Chapter',
        key: 'maxChapter',
        dataIndex: 'maxChapter',
        editable: title === EnumMangaProjectName.MAN_MIRROR,
      },
    ]

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
      title: 'LatestSync',
      key: 'latestSync',
      dataIndex: 'latestSync',
      render: (value) => {
        const backgroundColor = value ? getLatestSyncColor(value) : undefined
        return (
          <div
            style={{
              backgroundColor,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'baseline',
              padding: '10px',
              boxSizing: 'border-box',
            }}
          >
            <Typography.Text>
              {value ? dayjs(value).format('DD/MM/YY hh:mm:ss') : '-'}
            </Typography.Text>
          </div>
        )
      },
    })
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
                    cartoonDriveId: record.cartoonDriveId,
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
                disabled={
                  isUpdateConfigLoading ||
                  isDownloadMangaOneLoading ||
                  cartoonDownloadingIds.includes(record.cartoonId.toString()) ||
                  record.disabled
                }
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
    cartoonDownloadingIds,
    colorBgMask,
    colorSuccessActive,
    downloadMangaOne,
    downloadOneParams?.cartoonId,
    getColumnSearchProps,
    getLatestSyncColor,
    isDownloadMangaOneLoading,
    isUpdateConfigLoading,
    onCartoonIdClick,
    router,
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
    <ConfigProvider theme={themeConfig}>
      <Space ref={ref} className={warpCss} direction="vertical" size={8}>
        {!noHeader && <Typography.Title level={3}>{title}</Typography.Title>}
        <Table
          dataSource={dataSource}
          columns={columns as ColumnType<IItem>[]}
          rowKey={(d) => d.projectName + d.cartoonId}
          pagination={paginateOptions}
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
    </ConfigProvider>
  )
}
