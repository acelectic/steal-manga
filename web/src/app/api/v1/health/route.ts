import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const response = new NextResponse(null, {
    status: 200,
  })
  return response
}
