import { useMutation } from '@tanstack/react-query'
import { Button, Col, Form, Input, Modal, Row, Select, message } from 'antd'
import { pascalize } from 'humps'
import { values } from 'lodash'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { InputNumber } from '../../components/common/InputNumber'
import { updateMangaConfig } from '../../service/manga-updated'
import { EnumMangaProjectName, IMangaConfig } from '../../service/manga-updated/types'

interface IAddMangaConfigProps {}
export const AddMangaConfig = (props: IAddMangaConfigProps) => {
  const router = useRouter()

  const [modalVisible, setModalVisible] = useState(false)

  const { mutateAsync: addMangaConfig, isLoading } = useMutation(updateMangaConfig, {
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
  })

  return (
    <Row>
      <Col>
        <Button type="primary" onClick={setModalVisible.bind(null, true)} size="small">
          New Manga Config
        </Button>
      </Col>

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
        <AddMangaConfigForm
          onFinish={(values) => {
            return addMangaConfig({
              ...values,
              disabled: false,
              cartoonDriveId: '',
              downloaded: 0,
              maxChapter: values?.maxChapter || 0,
            })
          }}
          isLoading={isLoading}
          onCancelClick={setModalVisible.bind(null, false)}
        />
      </Modal>
    </Row>
  )
}

interface IAddMangaConfigFormProps {
  onFinish: (values: IMangaConfig) => void
  isLoading: boolean
  onCancelClick?: () => void
}
const AddMangaConfigForm = (props: IAddMangaConfigFormProps) => {
  const { onFinish, isLoading, onCancelClick } = props
  const [form] = Form.useForm<IMangaConfig>()
  const projectName = Form.useWatch('projectName', form)
  return (
    <Form<IMangaConfig> form={form} onFinish={onFinish} layout="vertical" disabled={isLoading}>
      <Form.Item name="projectName" label="ProjectName" required>
        <Select
          options={values(EnumMangaProjectName).map((project) => {
            return {
              value: project,
              label: pascalize(project),
            }
          })}
        />
      </Form.Item>
      <Form.Item name="cartoonName" label="CartoonName" required>
        <Input />
      </Form.Item>
      <Form.Item name="cartoonId" label="CartoonId" required>
        <Input />
      </Form.Item>
      <Form.Item
        name="latestChapter"
        label="LatestChapter"
        rules={[
          {
            type: 'number',
            min: 0,
            max: 1000,
          },
        ]}
        required
      >
        <InputNumber />
      </Form.Item>
      {projectName === EnumMangaProjectName.MAN_MIRROR && (
        <Form.Item
          name="maxChapter"
          label="MaxChapter"
          rules={[
            {
              type: 'number',
              min: 0,
              max: 1000,
            },
          ]}
          required
        >
          <InputNumber />
        </Form.Item>
      )}

      <Row gutter={[12, 12]} justify="end">
        <Col>
          <Button htmlType="button" onClick={onCancelClick} disabled={isLoading} block>
            Cancel
          </Button>
        </Col>
        <Col>
          <Button type="primary" htmlType="submit" loading={isLoading} disabled={isLoading} block>
            Save
          </Button>
        </Col>
      </Row>
    </Form>
  )
}
