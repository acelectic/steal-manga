import path from 'path'
import { Koyeb } from '../../modules/koyeb/Koyeb'
import { appConfig } from '../../config/app-config'
import qs from 'qs'
import { camelizeKeys } from 'humps'
import to from 'await-to-js'
import { IGetServiceResponse } from '../../service/koyeb/types'

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

const KoyebPage = async () => {
  const [, data] = await to(getKoYebService())
  console.log({ data: JSON.stringify(data) })
  return <Koyeb service={data?.service} />
}

export default KoyebPage
