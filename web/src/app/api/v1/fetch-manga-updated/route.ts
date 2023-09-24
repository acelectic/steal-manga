import to from 'await-to-js'
import { revalidatePath } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'
import { fetchMangaUpdated } from '../../../../service/fetch-manga-updated'

export async function POST(request: NextRequest) {
  const [, responseData] = await to(fetchMangaUpdated())

  const pathUrl = request.nextUrl.searchParams.get('path') || '/'

  revalidatePath(pathUrl)
  const response = new NextResponse(JSON.stringify(responseData), {
    status: 200,
  })
  return response
}
