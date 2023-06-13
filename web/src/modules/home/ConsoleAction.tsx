import { Button, Col, Row } from 'antd'
import {
  ITriggerDownloadPayload,
  TriggerDownloadTypeEnum,
} from '../../service/trigger-download/types'
import { useMutation } from '@tanstack/react-query'

export const ConsoleAction = () => {
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
    },
  )

  return (
    <Row gutter={[16, 16]}>
      <Col>
        <Button
          onClick={triggerDownload.bind(null, TriggerDownloadTypeEnum.MAN_MIRROR)}
          loading={isLoading}
          disabled={isLoading}
        >
          Download Man Mirror
        </Button>
      </Col>
      <Col>
        <Button
          onClick={triggerDownload.bind(null, TriggerDownloadTypeEnum.MY_NOVEL)}
          loading={isLoading}
          disabled={isLoading}
        >
          Download My Novel
        </Button>
      </Col>
    </Row>
  )
}
