import { Button, Col, Row } from 'antd'
import { useCallback, useMemo } from 'react'
import { openGoogleDrive } from '../../utils/helper'

type IDrivePortalItem =
  | {
      name: string
      driveId: string
    }
  | {
      name: string
      link: string
    }

export const DrivePortal = () => {
  const items = useMemo<IDrivePortalItem[]>(() => {
    return [
      {
        name: 'steal-manga',
        driveId: '1iXUAF2N3YxLPvJyDTYYL1f8HFP1mU1Ek',
      },
      {
        name: 'กิลด์บุรุษเที่ยงคืน',
        driveId: '1TA9Q7m5PeH1Qa-qRKb8poT7tflO0pjQ3',
      },
      {
        name: 'Man Mirror',
        link: 'https://www.manmirror.net/main.php?page=phome',
      },
      {
        name: 'My Novel',
        link: 'https://mynovel.co',
      },
    ]
  }, [])

  const onGoToDriveClick = useCallback((item: IDrivePortalItem) => {
    if ('driveId' in item) {
      openGoogleDrive(item.driveId)
    } else if ('link' in item) {
      window.open(item.link, '_blank')
    }
  }, [])

  return (
    <Row gutter={[12, 12]}>
      {items.map((item) => {
        return (
          <Col key={item.name}>
            <Button onClick={onGoToDriveClick.bind(null, item)}>{item.name}</Button>
          </Col>
        )
      })}
    </Row>
  )
}
