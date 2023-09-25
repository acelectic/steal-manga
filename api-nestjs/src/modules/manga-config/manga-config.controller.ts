import { Controller, Get } from '@nestjs/common'
import { ApiTags } from '@nestjs/swagger'
import { MangaConfigService } from './manga-config.service'

@ApiTags('manga-configs')
@Controller('manga-configs')
export class MangaConfigController {
  constructor(private readonly mangaConfigService: MangaConfigService) {}

  // @Post()
  // create(@Body() createMangaConfigDto: CreateMangaConfigDto) {
  //   return this.mangaConfigService.create(createMangaConfigDto)
  // }

  @Get()
  findAll() {
    return this.mangaConfigService.findAll()
  }

  // @Get(':id')
  // findOne(@Param('id') id: string) {
  //   return this.mangaConfigService.findOne(+id)
  // }

  // @Patch(':id')
  // update(
  //   @Param('id') id: string,
  //   @Body() updateMangaConfigDto: UpdateMangaConfigDto,
  // ) {
  //   return this.mangaConfigService.update(+id, updateMangaConfigDto)
  // }

  // @Delete(':id')
  // remove(@Param('id') id: string) {
  //   return this.mangaConfigService.remove(+id)
  // }
}
