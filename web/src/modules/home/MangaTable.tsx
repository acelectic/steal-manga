'use client'
import {
  Button,
  Col,
  Form,
  FormInstance,
  Input,
  InputRef,
  Row,
  Space,
  Switch,
  Table,
  Typography,
  message,
} from 'antd'
import { IGetMangaUpdatedResponse } from '../../service/manga-updated/types'
import React, { useContext, useEffect, useMemo, useRef, useState } from 'react'
import { ColumnType } from 'antd/es/table'
import { css } from '@emotion/css'
import { updateMangeConfig } from '../../service/manga-updated'
import { chain } from 'lodash'

const warpCss = css`
  width: 100%;

  .editable-cell {
    position: relative;
  }

  .editable-cell-value-wrap {
    padding: 5px 12px;
    cursor: pointer;
  }

  .editable-cell-value-wrap:hover {
    padding: 4px 11px;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
  }
`

const EditableContext = React.createContext<FormInstance<any> | null>(null)

interface IItem {
  cartoonName: string
  cartoonId: string
  latestChapter: number
  maxChapter: number
  disabled: boolean
  downloaded: number
}

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
    if (dataType === 'boolean') {
      if (Array.isArray(children)) {
        return chain(children)
          .map((e) => {
            if (typeof e === 'boolean') return e === true ? 'True' : 'False'
            return e
          })
          .value()
      }
    }
    return children
  }, [children, dataType])

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
}
export const MangaTable = (props: IMangaTableProps) => {
  const { title, data } = props
  const [dataSource, setDataSource] = useState<IItem[]>([])

  useEffect(() => {
    setDataSource(
      data.map(
        (e): IItem => ({
          cartoonName: e.cartoonName,
          cartoonId: e.cartoonId,
          latestChapter: e.latestChapter,
          maxChapter: +e.maxChapter,
          disabled: e.disabled,
          downloaded: e.downloaded,
        }),
      ),
    )
  }, [data])

  const defaultColumns = useMemo(
    (): (ColumnType<IItem> & Partial<Pick<EditableCellProps, 'editable' | 'dataType'>>)[] => [
      { title: 'Cartoon Name', key: 'cartoonName', dataIndex: 'cartoonName' },
      { title: 'Cartoon Id', key: 'cartoonId', dataIndex: 'cartoonId' },
      {
        title: 'Latest Chapter',
        key: 'latestChapter',
        dataIndex: 'latestChapter',
        editable: title === 'my-novel',
      },
      {
        title: 'Max Chapter',
        key: 'maxChapter',
        dataIndex: 'maxChapter',
        editable: title === 'man-mirror',
      },
      {
        title: 'Disabled',
        key: 'disabled',
        dataIndex: 'disabled',
        editable: true,
        dataType: 'boolean',
        render: (value: boolean) => !!value,
      },
      { title: 'Downloaded', key: 'downloaded', dataIndex: 'downloaded' },
      {
        title: 'Action',
        key: 'cartoonId',
        render(value, record, index) {
          return (
            <Button
              onClick={async () => {
                await updateMangeConfig({
                  projectName: title,
                  cartoonId: record.cartoonId,
                  cartoonName: record.cartoonName,
                  latestChapter: +record.latestChapter,
                  maxChapter: +record.maxChapter,
                  disabled: record.disabled,
                  downloaded: record.downloaded,
                })
                message.success('Update Config Success')
              }}
            >
              Save
            </Button>
          )
        },
      },
    ],
    [title],
  )

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
      <Typography.Title level={3}>{title}</Typography.Title>
      <Table
        dataSource={dataSource}
        columns={columns as ColumnType<IItem>[]}
        rowKey={'cartoonId'}
        pagination={{
          defaultPageSize: 5,
        }}
        components={{
          body: {
            row: EditableRow,
            cell: EditableCell,
          },
        }}
      />
    </Space>
  )
}
