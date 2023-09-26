import { ApiProperty } from '@nestjs/swagger'
import { IsEnum, IsNotEmpty } from 'class-validator'
import { EnumMangaConfigProjectName } from '../../../db/entities/MangaConfig'

export class DownLoadMangaOneParamsDto {
  @ApiProperty()
  @IsEnum(EnumMangaConfigProjectName)
  @IsNotEmpty()
  projectName: EnumMangaConfigProjectName
}
