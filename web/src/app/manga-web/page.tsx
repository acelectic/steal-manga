import { MangaWeb } from '../../modules/manga-web/MangaWeb'
import { DbClient } from '../../utils/db-client'

const MangaWebPage = async () => {
  const mangaWebQuery = await DbClient.init.table_manga_web.find()
  const rawData = await mangaWebQuery.toArray()
  const data = rawData.map((d) => {
    return {
      id: d.id,
      name: d.name,
      link: d.link,
    }
  })
  return <MangaWeb data={data} />
}

export default MangaWebPage
