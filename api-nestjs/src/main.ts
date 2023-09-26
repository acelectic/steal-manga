import { ValidationPipe, VersioningType } from '@nestjs/common'
import { NestFactory } from '@nestjs/core'
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger'
import 'dotenv/config'
import { json, urlencoded } from 'express'
import expressBasicAuth from 'express-basic-auth'
import { AppModule } from './app.module'
import appConfig from './config/app-config'
import './config/dayjs-config'
import { bullServerAdapter } from './modules/task/bull-board.provider'

async function bootstrap() {
  const app = await NestFactory.create(AppModule)
  app.enableVersioning({
    type: VersioningType.URI,
    prefix: 'v',
    defaultVersion: '1',
  })
  app.enableCors({
    origin: '*',
    methods: ['GET', 'PUT', 'PATCH', 'POST', 'DELETE', 'OPTIONS'],
    exposedHeaders: ['Content-Disposition'],
    credentials: true,
  })
  app.useGlobalPipes(
    new ValidationPipe({
      transform: true,
      whitelist: true,
    }),
  )
  // app.useGlobalInterceptors(new ClassSerializerInterceptor(app.get(Reflector)))

  app.setGlobalPrefix('/api')

  app.use(json({ limit: '100mb' }))
  app.use(urlencoded({ limit: '50mb', extended: true }))

  // swagger
  app.use(
    ['/swagger', '/swagger-json'],
    expressBasicAuth({
      users: {
        [appConfig.SWAGGER_USERNAME]: appConfig.SWAGGER_PASSWORD,
      },
      challenge: true,
    }),
  )
  const config = new DocumentBuilder()
    .setTitle('Steal Manga API')
    .setDescription('Steal Manga API description')
    .setVersion('1.0')
    .build()
  const document = SwaggerModule.createDocument(app, config)
  SwaggerModule.setup('/swagger', app, document)

  // bull board
  app.use(
    '/bull-board',
    expressBasicAuth({
      users: {
        [appConfig.BULL_BOARD_USERNAME]: appConfig.BULL_BOARD_PASSWORD,
      },
      challenge: true,
    }),
    bullServerAdapter.getRouter(),
  )
  bullServerAdapter.setBasePath('/bull-board')

  const port = appConfig.PORT
  await app.listen(port)

  console.debug(
    '\n',
    `Nest server is running`,
    `\n\tVersion: ${appConfig.VERSION}`,
    `\n\tPort: ${port}`,
    '\n',
  )
}
bootstrap()
