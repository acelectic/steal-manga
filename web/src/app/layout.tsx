import { Sarabun } from 'next/font/google'
import React from 'react'
import AppLayout from '../components/layouts/index.'
import AntdProvider from '../components/providers/AntdProvider'
import EmotionProvider from '../components/providers/EmotionProvider'
import { InitLogRocker } from '../components/providers/InitLogRocker'
import ReactQueryProvider from '../components/providers/ReactQueryProvider'
import SseProvider from '../components/providers/SseProvider'
import { appConfig } from '../config/app-config'
import './globals.css'
const inter = Sarabun({ weight: '400', subsets: ['thai'] })

export const metadata = {
  title: 'Manga Steal',
  description: '...',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className} style={{ minHeight: '100vh' }}>
        <AntdProvider>
          <EmotionProvider>
            <ReactQueryProvider>
              <SseProvider>
                <InitLogRocker
                  NEXT_PUBLIC_LOG_ROCKET_APP_ID={appConfig.NEXT_PUBLIC_LOG_ROCKET_APP_ID || ''}
                />
                <AppLayout>{children}</AppLayout>
              </SseProvider>
            </ReactQueryProvider>
          </EmotionProvider>
        </AntdProvider>
      </body>
    </html>
  )
}
