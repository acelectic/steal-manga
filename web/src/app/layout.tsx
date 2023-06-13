import { AppProvider } from './app-provider'
import RootStyleRegistry from './emotion'
import './globals.css'
import { Sarabun } from 'next/font/google'
import React from 'react'

const inter = Sarabun({ weight: '400', subsets: ['thai'] })

export const metadata = {
  title: 'Create Next App',
  description: 'Generated by create next app',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body
        className={inter.className}
        style={{
          backgroundColor: '#80bcdf',
          width: '100vw',
          height: '100vh',
        }}
      >
        <AppProvider>
          <RootStyleRegistry>{children}</RootStyleRegistry>
        </AppProvider>
      </body>
    </html>
  )
}
