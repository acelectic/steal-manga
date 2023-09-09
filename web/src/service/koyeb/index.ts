import { useQuery } from '@tanstack/react-query'
import { koyebClient } from '../../utils/http-client/koyeb-client'
import path from 'path'

const KOYEB_URL = 'koyeb'
const KOYEB_SERVICE_URL = 'services'

export const useGetKoYebServices = () => {
  return useQuery([KOYEB_URL, KOYEB_SERVICE_URL], async () => {
    const { data } = await koyebClient.get(KOYEB_SERVICE_URL)
    return data
  })
}

export const useGetKoYebService = (serviceId: string) => {
  return useQuery([KOYEB_URL, KOYEB_SERVICE_URL, { serviceId }], async () => {
    const { data } = await koyebClient.get(path.join(KOYEB_SERVICE_URL, serviceId))
    return data
  })
}
