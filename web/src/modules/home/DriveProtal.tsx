import { Button, Col, Row } from 'antd'
import { useCallback, useMemo } from 'react'

interface IDriveProtalItem {
  name: string
  driveId: string
}

export const DriveProtal = () => {
  const items = useMemo<IDriveProtalItem[]>(() => {
    return [
      {
        name: 'steal-manga',
        driveId: '1iXUAF2N3YxLPvJyDTYYL1f8HFP1mU1Ek',
      },
      {
        name: 'กิลด์บุรุษเที่ยงคืน',
        driveId: '1TA9Q7m5PeH1Qa-qRKb8poT7tflO0pjQ3',
      },
    ]
  }, [])

  const onGoToDriveClick = useCallback((driveId: string) => {
    const googleDriveLink = `https://drive.google.com/drive/u/0/folders/${driveId}`
    window.open(googleDriveLink, '_blank')
  }, [])

  return (
    <Row gutter={[12, 12]}>
      {items.map((item) => {
        return (
          <Col key={item.driveId}>
            <Button onClick={onGoToDriveClick.bind(null, item.driveId)}>{item.name}</Button>
          </Col>
        )
      })}
    </Row>
  )
}
