import {
  Controller,
  HttpCode,
  HttpStatus,
  Param,
  Post,
  Query,
  Req,
  Sse,
} from '@nestjs/common'
import { EventEmitter2 } from '@nestjs/event-emitter'
import { ApiTags } from '@nestjs/swagger'
import { Request } from 'express'
import { DownLoadMangaOneParamsDto } from './dto/download-manga-one'
import { MangaDownloadService } from './manga-download.service'

@ApiTags('manga-downloads')
@Controller('manga-downloads')
export class MangaDownloadController {
  constructor(
    private readonly mangaDownloadService: MangaDownloadService,
    private readonly eventService: EventEmitter2,
  ) {}

  @Sse('projects-status')
  getProjectDownloadStatus(
    @Req() req: Request,
    @Query() params: DownLoadMangaOneParamsDto,
  ) {
    return this.mangaDownloadService.getProjectDownloadStatus(
      req,
      params.projectName,
    )
  }

  @Sse('cartoons-status')
  getMangaDownloadStatus(@Req() req: Request) {
    return this.mangaDownloadService.getMangaDownloadStatus(req)
  }

  @HttpCode(HttpStatus.ACCEPTED)
  @Post('download/:projectName')
  async downloadMangaByProject(@Param() params: DownLoadMangaOneParamsDto) {
    const job = await this.mangaDownloadService.downloadMangaByProject(params)

    return {
      processId: job.id,
    }
  }
}
