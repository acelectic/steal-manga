import { Injectable, MessageEvent } from '@nestjs/common'
import { EventEmitter2 } from '@nestjs/event-emitter'
import { InjectModel } from '@nestjs/mongoose'
import { Request } from 'express'
import { chain, round } from 'lodash'
import { AnyBulkWriteOperation } from 'mongodb'
import { Model } from 'mongoose'
import { Subject, map } from 'rxjs'
import { AppRedisClient } from '../../config/cache-module-config'
import {
  EnumMangaConfigProjectName,
  MangaConfig,
} from '../../db/entities/MangaConfig'
import { MangaUpload } from '../../db/entities/MangaUpload'
import { MangaPythonService } from '../manga-python-service/manga-python-service.service'
import { TaskCommand } from '../task/task.command'
import { DownLoadMangaOneParamsDto } from './dto/download-manga-one'

@Injectable()
export class MangaDownloadService {
  constructor(
    @InjectModel(MangaConfig.name) private mangaConfigModel: Model<MangaConfig>,
    @InjectModel(MangaUpload.name) private mangaUploadModel: Model<MangaUpload>,
    private readonly mangaPythonService: MangaPythonService,
    private readonly appRedisClient: AppRedisClient,
    private readonly eventService: EventEmitter2,
    private readonly taskCommand: TaskCommand,
  ) {}

  async updateLatestSync() {
    const mangaConfigs = await this.mangaConfigModel.find()
    const bulkUpdateConfig: AnyBulkWriteOperation<MangaConfig>[] = []
    for (const mangaConfig of mangaConfigs) {
      const { project_name, cartoon_id } = mangaConfig
      const latestMangaUpload = await this.mangaUploadModel.findOne(
        {
          project_name,
          cartoon_id,
        },
        {
          project_name: 1,
          cartoon_id: 1,
          created_time: 1,
        },
        {
          sort: {
            created_time: -1,
          },
        },
      )
      console.log({
        latestMangaUpload: latestMangaUpload.toJSON(),
      })
      const latest_sync = latestMangaUpload.created_time
      bulkUpdateConfig.push({
        updateOne: {
          filter: {
            project_name,
            cartoon_id,
          },
          update: {
            $set: {
              latest_sync,
            },
          },
        },
      })
    }

    await this.mangaConfigModel.bulkWrite(bulkUpdateConfig)
  }

  async downloadMangaByProject(params: DownLoadMangaOneParamsDto) {
    return this.taskCommand.downloadMangaByProject(params)
  }

  // for job
  async performDownloadMangaByProject(
    params: DownLoadMangaOneParamsDto,
    onProgress: (progress: number) => Promise<void>,
  ) {
    const { projectName } = params
    const projectDownloadKey = this.getProjectDownloadKey(projectName)
    const downloadingKey = this.getCartoonDownloadKey()
    const mangaConfigs = await this.mangaConfigModel.find({
      project_name: projectName,
      disabled: false,
    })

    await this.appRedisClient.set(projectDownloadKey, mangaConfigs.length)
    const cartoonDownloadingIds = chain(mangaConfigs)
      .map((e) => e.cartoon_id.toString())
      .compact()
      .value()
    if (cartoonDownloadingIds.length) {
      await this.appRedisClient.sadd(downloadingKey, ...cartoonDownloadingIds)
    } else {
      await this.appRedisClient.sadd(downloadingKey, '-99999')
    }

    let i = 1
    for (const mangaConfig of mangaConfigs) {
      const { cartoon_id, cartoon_name } = mangaConfig
      console.log('before call api ' + cartoon_name)
      await this.mangaPythonService.downloadMangaOne(mangaConfig._id.toString())
      console.log('after call api')
      await this.appRedisClient.srem(downloadingKey, cartoon_id.toString())
      console.log('after srem')
      await this.appRedisClient.set(projectDownloadKey, mangaConfigs.length - i)
      console.log('after set')

      i += 1
      await onProgress(round((i / mangaConfigs.length) * 100, 2))
      console.log('after onProgress')
    }

    await this.appRedisClient.del(projectDownloadKey)
    console.log('after del')

    return {
      mangaConfigs: mangaConfigs.map((d) => d.toJSON()),
    }
  }

  getProjectDownloadStatus(
    req: Request,
    projectName: EnumMangaConfigProjectName,
  ) {
    const key = this.getProjectDownloadKey(projectName)
    const eventKey = 'project-download'
    const subject = new Subject()
    this.eventService.on(eventKey, (data) => {
      if (data.projectName === projectName) subject.next(data)
    })

    const intervalId = setInterval(async () => {
      const downloadRemain = await this.appRedisClient.get(key)
      this.eventService.emit(eventKey, {
        downloadRemain: Number(downloadRemain || 0),
        projectName,
      })
    }, 5 * 1000)

    req.on('close', () => {
      clearInterval(intervalId)
    })

    return subject.pipe(map((data: string): MessageEvent => ({ data })))
  }

  getMangaDownloadStatus(req: Request) {
    const key = this.getCartoonDownloadKey()

    const eventKey = 'cartoon-downloads'
    const subject = new Subject()
    this.eventService.on(eventKey, (data) => {
      if (data) subject.next(data)
    })

    const intervalId = setInterval(async () => {
      const cartoonDownloadingIds = await this.appRedisClient.smembers(key)
      this.eventService.emit(eventKey, {
        cartoonDownloadingIds: cartoonDownloadingIds || [],
      })
    }, 5 * 1000)

    req.on('close', () => {
      clearInterval(intervalId)
    })

    return subject.pipe(map((data: string): MessageEvent => ({ data })))
  }

  private getProjectDownloadKey(projectName: EnumMangaConfigProjectName) {
    return `project-downloading:${projectName}`
  }

  private getCartoonDownloadKey() {
    return `cartoons-downloading`
  }
}
