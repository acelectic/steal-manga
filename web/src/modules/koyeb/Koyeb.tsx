import path from 'path'
import { appConfig } from '../../config/app-config'
import { IKoyebService } from '../../service/koyeb/types'
import { camelizeKeys } from 'humps'

const callApi = async (
  action: 'pause' | 'resume' | 'redeploy',
  serviceId: string,
  options?: RequestInit,
) => {
  const response = await fetch(
    path.join(appConfig.KOYEB_API_HOST, 'v1', 'services', serviceId, action),
    {
      method: 'POST',
      headers: {
        Authorization: 'Bearer ' + appConfig.KOYEB_API_KEY,
      },
      ...options,
    },
  )
  const responseData = await response.json()
  return camelizeKeys(responseData)
}

interface IKoyebProps {
  service?: IKoyebService
}
export const Koyeb = (props: IKoyebProps) => {
  const { service } = props

  return (
    <div>
      <h2>{service?.name}</h2>
      <h4>Messages: {service?.messages}</h4>
      <h4>Status: {service?.status}</h4>
      {!!service && (
        <button
          onClick={() => {
            callApi('pause', service.id)
          }}
        >
          pause
        </button>
      )}
      {!!service && (
        <button
        // onClick={() => {
        //   callApi(service.id)
        // }}
        >
          resume
        </button>
      )}
      {!!service && (
        <button
        // onClick={() => {
        //   callApi(service.id)
        // }}
        >
          redeploy
        </button>
      )}
    </div>
  )
}
