import { RequestMethod } from '@nestjs/common'
import { Params } from 'nestjs-pino'

export const httpLoggerConfig: Params = {
  pinoHttp: {
    level: 'info',
    redact: {
      paths: ['req.body.password', 'req.headers.authorization'],
      censor: '********',
    },
    serializers: {
      req(req) {
        req.body = req.raw.body
        return req
      },
    },
  },
  exclude: [{ method: RequestMethod.GET, path: '/api/v1/health' }],
}
