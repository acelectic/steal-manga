import to from 'await-to-js'
import { NextRequest, NextResponse } from 'next/server'
import path from 'path'
import { appConfig } from '../../../../config/app-config'
import { decamelizeKeys } from 'humps'
import { revalidatePath } from 'next/cache'
import { triggerDownloadManga } from '../../../../service/trigger-download'

export async function POST(request: NextRequest) {
  const payload = await request.json()
  console.log({ payload })
  const [error, responseData] = await to(triggerDownloadManga(payload))
  console.log({ error })

  const dataRes = await responseData?.json()
  console.log({ dataRes })
  const pathUrl = request.nextUrl.searchParams.get('path') || '/'
  console.log({ pathUrl })

  revalidatePath(pathUrl)
  const response = new NextResponse(JSON.stringify(dataRes), {
    status: 200,
  })
  return response
}
