import path from 'path'
import { appConfig } from '../config/app-config'

export const BASE_API_URL = path.join(appConfig.API_HOST, 'api', 'v1')
