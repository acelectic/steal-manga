import path from 'path'
import { appConfig } from '../../config/app-config'
import { camelizeKeys } from 'humps'
import to from 'await-to-js'
import { IGetServiceResponse } from '../../service/koyeb/types'

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

const getKoYebService = async (options?: RequestInit) => {
  const response = await fetch(
    path.join(appConfig.KOYEB_API_HOST, 'v1', 'services', appConfig.KOYEB_API_SERVICE_ID),
    {
      headers: {
        Authorization: 'Bearer ' + appConfig.KOYEB_API_KEY,
      },
      ...options,
    },
  )
  const responseData = await response.json()
  return camelizeKeys(responseData) as IGetServiceResponse
}

// async function pauseService(serviceId: string) {
//   'use server'
//   callApi('pause', serviceId)
// }
// async function resumeService(serviceId: string) {
//   'use server'
//   callApi('resume', serviceId)
// }
// async function redeployService(serviceId: string) {
//   'use server'
//   callApi('redeploy', serviceId)
// }

// const action = async (formData: FormData) => {
//   'use server'
//   const serviceId = formData.get('serviceId')?.toString()
//   const type: any = formData.get('type')?.toString()
//   console.log({ serviceId, type })
//   if (serviceId && type) callApi(type, serviceId)
// }

const KoyebPage = async () => {
  const [, data] = await to(getKoYebService())
  console.log({ data: JSON.stringify(data) })
  const service = data?.service

  return (
    <div>
      <h2>{service?.name}</h2>
      <h4>Messages: {service?.messages}</h4>
      <h4>Status: {service?.status}</h4>
      {/* <form action={action}>
        <input name="type" value="pause" style={{ display: 'none' }} />
        <button type="submit">pause</button>
      </form> */}
      {/* {!!service?.id && <button onClick={pauseService.bind(null, service.id)}>pause</button>}
      {!!service?.id && <button onClick={resumeService.bind(null, service.id)}>resume</button>}
      {!!service?.id && <button onClick={redeployService.bind(null, service.id)}>redeploy</button>} */}
    </div>
  )
}

export default KoyebPage
