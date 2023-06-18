import to from 'await-to-js'
import { getMangaUpdated } from '../../service/manga-updated'
import { Table } from 'antd'
import dayjs from 'dayjs'

export const revalidate = 5

const PageMangaList = async () => {
  const [, data] = await to(
    getMangaUpdated({
      // cache: 'no-store',
      // // cache: 'only-if-cached',
      //   next: {
      //     // revalidate: 30,
      //     tags: ['manga-list'],
      //   },
    }),
  )

  return (
    <div>
      <p style={{ color: 'red' }}>{data?.updated}</p>
      <ul>
        {data?.resultsYetViewSorted.map(([updated, items]) => {
          return <li key={dayjs(updated).format()}>{dayjs(updated).format()}</li>
        })}
      </ul>
    </div>
  )
}

export default PageMangaList
