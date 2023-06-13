import { Home } from '../../modules/home/Home'
import to from 'await-to-js'
import { getMangaUpdated } from '../../service/manga-updated'

export const revalidate = 15

const HomePage = async () => {
  const [, data] = await to(
    getMangaUpdated({
      // cache: 'no-store',
      // // cache: 'only-if-cached',
      next: {
        revalidate: 30,
      },
    }),
  )

  return <Home data={data} />
}

export default HomePage
