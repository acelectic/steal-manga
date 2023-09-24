'use client'

import { css } from '@emotion/css'
import { useMutation } from '@tanstack/react-query'
import { Button, Col, Form, Input, Modal, Row, message } from 'antd'
import axios from 'axios'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { v4 } from 'uuid'
import { IMangaWebData, IUpdateMangaWebPayload } from '../../utils/db-client/collection-interface'
import { MangaWebTable } from './MangaWebTable'

const layoutCss = css`
  padding: 20px;
`

interface IMangaWebProps {
  data: IMangaWebData[]
}

export const MangaWeb = (props: IMangaWebProps) => {
  const { data } = props

  const router = useRouter()
  const [modalVisible, setModalVisible] = useState(false)

  const { mutateAsync: saveMangaWeb, isLoading } = useMutation(
    async (payload: IUpdateMangaWebPayload) => {
      const { data } = await axios.post('api/v1/manga-webs', {
        data: payload,
      })

      return data
    },
    {
      onSettled() {
        setModalVisible(false)
        router.refresh()

        setTimeout(() => {
          router.refresh()
        }, 1000)
      },
      onError() {
        message.error('Save Failed')
      },
    },
  )
  return (
    <div className={layoutCss}>
      <Row gutter={[16, 16]}>
        <Col>
          <Button onClick={setModalVisible.bind(null, true)} size="small">
            New
          </Button>
        </Col>
        <Col span={24}>
          <MangaWebTable data={data} />
        </Col>
      </Row>
      <Modal
        open={modalVisible}
        onCancel={setModalVisible.bind(null, false)}
        closable={false}
        okButtonProps={{
          style: {
            display: 'none',
          },
        }}
        footer={false}
        confirmLoading={isLoading}
        destroyOnClose
      >
        <Form<IMangaWebData>
          onFinish={(values) => {
            return saveMangaWeb({
              mangaWebs: [
                {
                  id: v4(),
                  name: values.name,
                  link: values.link,
                },
              ],
            })
          }}
          layout="vertical"
          disabled={isLoading}
        >
          <Form.Item name="name" label="Name" required>
            <Input />
          </Form.Item>
          <Form.Item name="link" label="Url" required>
            <Input inputMode="url" />
          </Form.Item>
          <Row gutter={[12, 12]} justify="end">
            <Col>
              <Button
                htmlType="button"
                onClick={setModalVisible.bind(null, false)}
                disabled={isLoading}
                block
              >
                Cancel
              </Button>
            </Col>
            <Col>
              <Button
                type="primary"
                htmlType="submit"
                loading={isLoading}
                disabled={isLoading}
                block
              >
                Save
              </Button>
            </Col>
          </Row>
        </Form>
      </Modal>
    </div>
  )
}
