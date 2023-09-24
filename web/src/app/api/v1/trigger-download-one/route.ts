import to from 'await-to-js'
import { revalidatePath } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'
import { downloadMangaOne } from '../../../../service/trigger-download'

export async function POST(request: NextRequest) {
  const payload = await request.json()
  const [, responseData] = await to(downloadMangaOne(payload))

  const dataRes = await responseData?.json()
  let pathUrl = request.nextUrl.searchParams.get('path')

  if (!pathUrl) {
    pathUrl = '/'
  }

  revalidatePath(pathUrl)
  const response = new NextResponse(JSON.stringify(dataRes), {
    status: 200,
  })
  return response
}
