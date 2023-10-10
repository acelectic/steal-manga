import to from 'await-to-js'
import { Home } from '../../modules/home/Home'
import { getAuthGoogleStatus } from '../../service/auth'
import { getMangaUpdated } from '../../service/manga-updated'
import { DbClient } from '../../utils/db-client'

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

  const mangaWebQuery = await DbClient.init.table_manga_upload.find()
  const rawMangaUploads = await mangaWebQuery.toArray()
  const mangaUploads = rawMangaUploads.map((d) => {
    return {
      ...d,
      _id: d._id.toString(),
    }
  })

  return (
    <Home
      data={data}
      authGoogleStatus={!!dataGoogleStatus?.googleAuthenStatus}
      mangaUploads={mangaUploads}
    />
  )
}

export default HomePage
