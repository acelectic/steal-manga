import { PartialType } from '@nestjs/mapped-types'
import { CreateMangaConfigDto } from './create-manga-config.dto'

export class UpdateMangaConfigDto extends PartialType(CreateMangaConfigDto) {}
