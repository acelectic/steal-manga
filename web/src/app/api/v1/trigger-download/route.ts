import to from 'await-to-js'
import { revalidatePath } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'
import { triggerDownloadManga } from '../../../../service/trigger-download'

export async function POST(request: NextRequest) {
  const payload = await request.json()
  const [, responseData] = await to(triggerDownloadManga(payload))

  const dataRes = await responseData?.json()
  const pathUrl = request.nextUrl.searchParams.get('path') || '/'

  revalidatePath(pathUrl)
  const response = new NextResponse(JSON.stringify(dataRes), {
    status: 200,
  })
  return response
}
