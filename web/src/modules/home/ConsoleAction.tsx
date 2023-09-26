import { useMutation } from '@tanstack/react-query'
import { Button, Col, Row, Typography, message } from 'antd'
import { pascalizeKeys } from 'humps'
import { isEqual } from 'lodash'
import { useRouter } from 'next/navigation'
import { PropsWithChildren, useEffect, useState } from 'react'
import {
  ITriggerDownloadPayload,
  TriggerDownloadTypeEnum,
} from '../../service/trigger-download/types'

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

  const { mutateAsync: fetchMangaUpdated, isLoading: isFetchMangaUpdatedLoading } = useMutation(
    async () => {
      await fetch('/api/v1/fetch-manga-updated', {
        method: 'POST',
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
          'Content-Type': 'application/json',
        },
      })
    },
    {
      onSuccess: () => {
        message.success(`Fetch Manga Updated`)
        router.refresh()
      },
    },
  )
  return (
    <Row gutter={[16, 16]}>
      <Col span={24}>
        <Row>
          <Typography>Download</Typography>
        </Row>
      </Col>
      <Col>
        {/* <Button
          type="primary"
          onClick={triggerDownload.bind(null, [TriggerDownloadTypeEnum.MAN_MIRROR])}
          loading={isEqual(typesDownloading, [TriggerDownloadTypeEnum.MAN_MIRROR])}
          disabled={isLoading}
        >
          Man Mirror
        </Button> */}
        <ProjectActionButton
          projectName={TriggerDownloadTypeEnum.MAN_MIRROR}
          onClick={triggerDownload.bind(null, [TriggerDownloadTypeEnum.MAN_MIRROR])}
          isLoading={isEqual(typesDownloading, [TriggerDownloadTypeEnum.MAN_MIRROR])}
          disabled={isLoading}
        >
          Man Mirror
        </ProjectActionButton>
      </Col>
      <Col>
        {/* <Button
          type="primary"
          onClick={triggerDownload.bind(null, [TriggerDownloadTypeEnum.MY_NOVEL])}
          loading={isEqual(typesDownloading, [TriggerDownloadTypeEnum.MY_NOVEL])}
          disabled={isLoading}
        >
          My Novel
        </Button> */}
        <ProjectActionButton
          projectName={TriggerDownloadTypeEnum.MY_NOVEL}
          onClick={triggerDownload.bind(null, [TriggerDownloadTypeEnum.MY_NOVEL])}
          isLoading={isEqual(typesDownloading, [TriggerDownloadTypeEnum.MY_NOVEL])}
          disabled={isLoading}
        >
          My Novel
        </ProjectActionButton>
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
      <Col>
        <Button
          type="primary"
          color="#ddff1f"
          onClick={async () => {
            await fetchMangaUpdated()
          }}
          loading={isFetchMangaUpdatedLoading}
          disabled={isFetchMangaUpdatedLoading}
        >
          Fetch Updates
        </Button>
      </Col>
    </Row>
  )
}

interface IProjectActionButtonProps {
  projectName: TriggerDownloadTypeEnum
  onClick: () => void
  isLoading?: boolean
  disabled?: boolean
}
const ProjectActionButton = (props: PropsWithChildren<IProjectActionButtonProps>) => {
  const { projectName, onClick, disabled, isLoading, children } = props

  const [isDownloading, setIsDownloading] = useState(false)

  useEffect(() => {
    const eventSource = new EventSource(
      `${process.env.NEXT_PUBLIC_API_HOST}/api/v1/manga-downloads/projects-status?projectName=${projectName}`,
    )
    eventSource.onmessage = ({ data: dataString }) => {
      const data = JSON.parse(dataString)
      const { downloadRemain } = data

      setIsDownloading(!!downloadRemain)
    }

    return () => {
      eventSource.close()
    }
  }, [projectName])

  return (
    <Button
      type="primary"
      onClick={onClick}
      loading={isLoading || isDownloading}
      disabled={disabled || isDownloading}
    >
      {children}
    </Button>
  )
}
