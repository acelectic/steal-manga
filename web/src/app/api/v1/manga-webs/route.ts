import { HttpStatusCode } from 'axios'
import { Type, plainToClass } from 'class-transformer'
import {
  IsArray,
  IsNotEmpty,
  IsOptional,
  IsString,
  IsUrl,
  ValidateNested,
  validate,
} from 'class-validator'
import { revalidatePath } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'
import 'reflect-metadata'
import { DbClient } from '../../../../utils/db-client'
import {
  IMangaWebData,
  IUpdateMangaWebPayload,
} from '../../../../utils/db-client/collection-interface'

class MangaWebData
  implements Pick<IUpdateMangaWebPayload['mangaWebs'][number], 'name' | 'link' | 'id'>
{
  @IsString()
  @IsNotEmpty()
  id: string

  @IsString()
  @IsNotEmpty()
  name: string

  @IsString()
  @IsUrl()
  @IsOptional()
  link: string
}

class UpdateMangaWebData implements IUpdateMangaWebPayload {
  @ValidateNested({ each: true })
  @Type(() => MangaWebData)
  @IsArray()
  mangaWebs: IMangaWebData[]
}

export async function POST(request: NextRequest) {
  const rawData = await request.json()
  const data = plainToClass(UpdateMangaWebData, rawData.data)
  const validateResult = await validate(data)

  if (validateResult.length) {
    return NextResponse.json(
      {
        errors: validateResult,
      },
      {
        status: HttpStatusCode.UnprocessableEntity,
      },
    )
  }
  const result = await DbClient.init.updateBookmarkMangaWeb(data.mangaWebs)
  const { insertedCount, modifiedCount, upsertedCount } = result
  // const dataRes = await responseData?.json()
  const pathUrl = request.nextUrl.searchParams.get('path') || '/'
  revalidatePath(pathUrl)

  return NextResponse.json(
    {
      insertedCount,
      modifiedCount,
      upsertedCount,
      revalidated: true,
    },
    {
      status: HttpStatusCode.Ok,
    },
  )
}
