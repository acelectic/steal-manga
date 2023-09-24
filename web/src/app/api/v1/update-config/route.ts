import to from 'await-to-js'
import { decamelizeKeys } from 'humps'
import { revalidateTag } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'
import path from 'path'
import { appConfig } from '../../../../config/app-config'

export async function POST(request: NextRequest) {
  const payload = await request.json()
  revalidateTag('manga-list')
  console.log({ payload })
  const [error, responseData] = await to(
    fetch(path.join(appConfig.API_HOST, 'api', 'v1', 'manga-updated'), {
      method: 'POST',
      body: JSON.stringify(decamelizeKeys(payload)),
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    }),
  )

  const dataRes = await responseData?.json()

  return NextResponse.json(
    { ...dataRes, revalidated: true },
    {
      status: 200,
    },
  )
}
