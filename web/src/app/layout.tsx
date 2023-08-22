import ReactQueryProvider from '../components/providers/ReactQueryProvider'
import EmotionProvider from '../components/providers/EmotionProvider'
import './globals.css'
import { Sarabun } from 'next/font/google'
import React from 'react'
import AntdProvider from '../components/providers/AntdProvider'
import AppLayout from '../components/layouts/index.'
import { InitLogRocker } from '../components/providers/InitLogRocker'
import { appConfig } from '../config/app-config'
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
              <InitLogRocker
                NEXT_PUBLIC_LOG_ROCKET_APP_ID={appConfig.NEXT_PUBLIC_LOG_ROCKET_APP_ID || ''}
              />
              <AppLayout>{children}</AppLayout>
            </ReactQueryProvider>
          </EmotionProvider>
        </AntdProvider>
      </body>
    </html>
  )
}
