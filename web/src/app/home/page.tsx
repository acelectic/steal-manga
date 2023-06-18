import { Home } from '../../modules/home/Home'
import to from 'await-to-js'
import { getMangaUpdated } from '../../service/manga-updated'
import { getAuthGoogleStatus } from '../../service/auth'

export const revalidate = 15

const HomePage = async () => {
  const [, data] = await to(
    getMangaUpdated({
      // cache: 'no-store',
      // // cache: 'only-if-cached',
      // next: {
      //   // revalidate: 30,
      //   // tags: ['manga-list'],
      // },
    }),
  )

  const [, dataGoogleStatus] = await to(getAuthGoogleStatus())

  return <Home data={data} authGoogleStatus={!!dataGoogleStatus?.googleAuthenStatus} />
}

export default HomePage
