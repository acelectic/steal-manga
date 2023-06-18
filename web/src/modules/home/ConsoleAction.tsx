import { Button, Col, Row, message } from 'antd'
import {
  ITriggerDownloadPayload,
  TriggerDownloadTypeEnum,
} from '../../service/trigger-download/types'
import { useMutation } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'
import { pascalize } from 'humps'

export const ConsoleAction = () => {
  const router = useRouter()
  const { mutate: triggerDownload, isLoading } = useMutation(
    async (type: TriggerDownloadTypeEnum) => {
      const payload: ITriggerDownloadPayload = {
        type,
      }
      await fetch('/api/v1/trigger-download', {
        method: 'POST',
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
          'Content-Type': 'application/json',
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify(payload),
      })

      message.success(`Download ${pascalize(type)} Success`)
    },
  )

  return (
    <Row gutter={[16, 16]}>
      <Col>
        <Button
          type="primary"
          onClick={triggerDownload.bind(null, TriggerDownloadTypeEnum.MAN_MIRROR)}
          loading={isLoading}
          disabled={isLoading}
        >
          Download Man Mirror
        </Button>
      </Col>
      <Col>
        <Button
          type="primary"
          onClick={triggerDownload.bind(null, TriggerDownloadTypeEnum.MY_NOVEL)}
          loading={isLoading}
          disabled={isLoading}
        >
          Download My Novel
        </Button>
      </Col>

      {/* <Col>
        <Button
          onClick={() => {
            router.refresh()
          }}
          loading={isLoading}
          disabled={isLoading}
        >
          Download My Novel
        </Button>
      </Col> */}
    </Row>
  )
}
