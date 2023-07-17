import { Button, Col, Row, Typography, message } from 'antd'
import {
  ITriggerDownloadPayload,
  TriggerDownloadTypeEnum,
} from '../../service/trigger-download/types'
import { useMutation } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'
import { pascalize, pascalizeKeys } from 'humps'
import { css } from '@emotion/css'
import { useState } from 'react'
import { intersection, isEqual } from 'lodash'

export const ConsoleAction = () => {
  const router = useRouter()
  const [typesDownloading, setTypesDownloading] = useState<TriggerDownloadTypeEnum[]>([])
  const { mutate: triggerDownload, isLoading } = useMutation(
    async (types: TriggerDownloadTypeEnum[]) => {
      setTypesDownloading(types)
      const payload: ITriggerDownloadPayload = {
        types,
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
      setTypesDownloading([])
      message.success(`Download ${pascalizeKeys(types)} Success`)
    },
  )

  return (
    <Row gutter={[16, 16]}>
      <Col span={24}>
        <Row>
          <Typography>Download</Typography>
          <pre>{JSON.stringify(typesDownloading)}</pre>
        </Row>
      </Col>
      <Col>
        <Button
          type="primary"
          onClick={triggerDownload.bind(null, [TriggerDownloadTypeEnum.MAN_MIRROR])}
          loading={isEqual(typesDownloading, [TriggerDownloadTypeEnum.MAN_MIRROR])}
          disabled={isLoading}
        >
          Man Mirror
        </Button>
      </Col>
      <Col>
        <Button
          type="primary"
          onClick={triggerDownload.bind(null, [TriggerDownloadTypeEnum.MY_NOVEL])}
          loading={isEqual(typesDownloading, [TriggerDownloadTypeEnum.MY_NOVEL])}
          disabled={isLoading}
        >
          My Novel
        </Button>
      </Col>
      <Col>
        <Button
          type="primary"
          onClick={triggerDownload.bind(null, [
            TriggerDownloadTypeEnum.MAN_MIRROR,
            TriggerDownloadTypeEnum.MY_NOVEL,
          ])}
          loading={isEqual(typesDownloading, [
            TriggerDownloadTypeEnum.MAN_MIRROR,
            TriggerDownloadTypeEnum.MY_NOVEL,
          ])}
          disabled={isLoading}
        >
          Both
        </Button>
      </Col>
    </Row>
  )
}
