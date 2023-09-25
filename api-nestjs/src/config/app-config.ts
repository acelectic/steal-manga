import 'dotenv/config'
import Joi from 'joi'

export const ALLOW_NODE_ENV = [
  'development',
  'staging',
  'uat',
  'production',
] as const

const appConfig = {
  NODE_ENV: process.env.NODE_ENV as (typeof ALLOW_NODE_ENV)[number],
  APP_MODE: process.env.APP_MODE as (typeof ALLOW_NODE_ENV)[number],
  VERSION: process.env.VERSION || '',
  IS_WORKER: process.env.IS_WORKER === 'true',
  SECRET_KEY: process.env.SECRET_KEY,
  DEBUG: process.env.DEBUG === 'true',
  GH_TOKEN: process.env.GH_TOKEN,
  UPDATE_MINUTE_THRESHOLD: +process.env.UPDATE_MINUTE_THRESHOLD,
  DRIVE_CARTOONS_DIR_ID: process.env.DRIVE_CARTOONS_DIR_ID,
  DELETE_FILE_AFTER_UPLOADED: process.env.DELETE_FILE_AFTER_UPLOADED === 'true',
  APP_URL: process.env.APP_URL,
  WEB_URL: process.env.WEB_URL,
  GOOGLE_AUTH_TYPE: process.env.GOOGLE_AUTH_TYPE,
  GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID,
  GOOGLE_PROJECT_ID: process.env.GOOGLE_PROJECT_ID,
  GOOGLE_CLIENT_SECRET: process.env.GOOGLE_CLIENT_SECRET,
  GOOGLE_REDIRECT_URIS: process.env.GOOGLE_REDIRECT_URIS?.split(','),
  GOOGLE_JAVASCRIPT_ORIGINS: process.env.GOOGLE_JAVASCRIPT_ORIGINS?.split(','),
  DB_USERNAME: process.env.DB_USERNAME,
  DB_PASSWORD: process.env.DB_PASSWORD,
  DB_NAME: process.env.DB_NAME,
  SWAGGER_USERNAME: process.env.SWAGGER_USERNAME,
  SWAGGER_PASSWORD: process.env.SWAGGER_PASSWORD,
  BULL_BOARD_USERNAME: process.env.BULL_BOARD_USERNAME,
  BULL_BOARD_PASSWORD: process.env.BULL_BOARD_PASSWORD,
  REDIS_HOST: process.env.REDIS_HOST,
  REDIS_PORT: +process.env.REDIS_PORT,
  REDIS_PREFIX: process.env.REDIS_PREFIX,
}

type IConfigKey = keyof typeof appConfig
type IJoiObject = { [p in IConfigKey]: Joi.Schema<unknown> }

const joiObject: IJoiObject = {
  NODE_ENV: Joi.string().valid(...ALLOW_NODE_ENV),
  APP_MODE: Joi.string().valid(...ALLOW_NODE_ENV),
  VERSION: Joi.string().optional(),
  IS_WORKER: Joi.boolean().optional(),
  SECRET_KEY: Joi.string().required(),
  DEBUG: Joi.boolean().optional(),
  GH_TOKEN: Joi.string().optional(),
  UPDATE_MINUTE_THRESHOLD: Joi.number().required(),
  DRIVE_CARTOONS_DIR_ID: Joi.string().required(),
  DELETE_FILE_AFTER_UPLOADED: Joi.boolean().required(),
  APP_URL: Joi.string().required(),
  WEB_URL: Joi.string().required(),
  GOOGLE_AUTH_TYPE: Joi.string().required(),
  GOOGLE_CLIENT_ID: Joi.string().required(),
  GOOGLE_PROJECT_ID: Joi.string().required(),
  GOOGLE_CLIENT_SECRET: Joi.string().required(),
  GOOGLE_REDIRECT_URIS: Joi.string().required(),
  GOOGLE_JAVASCRIPT_ORIGINS: Joi.string().required(),
  DB_USERNAME: Joi.string().required(),
  DB_PASSWORD: Joi.string().required(),
  DB_NAME: Joi.string().required(),
  SWAGGER_USERNAME: Joi.string().required(),
  SWAGGER_PASSWORD: Joi.string().required(),
  BULL_BOARD_USERNAME: Joi.string().required(),
  BULL_BOARD_PASSWORD: Joi.string().required(),
  REDIS_HOST: Joi.string().required(),
  REDIS_PORT: Joi.number().required(),
  REDIS_PREFIX: Joi.string().required(),
}

export const validationEnvSchema = Joi.object<IJoiObject>(joiObject)

export default appConfig
