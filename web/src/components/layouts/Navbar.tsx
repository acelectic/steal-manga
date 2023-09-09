'use client'

import { Button, Menu } from 'antd'
import { Header } from 'antd/es/layout/layout'
import { MenuItemType } from 'antd/es/menu/hooks/useItems'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

const Navbar = () => {
  const router = useRouter()
  const items: MenuItemType[] = [
    {
      key: 'home',
      label: <Link href="/home">Home</Link>,
    },
    {
      key: 'koyeb',
      label: <Link href="/koyeb">Koyeb</Link>,
    },
    {
      key: 'Refresh',
      label: (
        <Button type="primary" onClick={router.refresh.bind(null)}>
          Refresh
        </Button>
      ),
    },
  ]
  return (
    <Header>
      <Menu theme="dark" mode="horizontal" items={items} />
    </Header>
  )
}

export default Navbar
