import { CartoonList } from '../../../modules/cartoon/CartoonList'
import { DbClient } from '../../../utils/db-client'
import { IMangaUpload } from '../../../utils/db-client/collection-interface'

const CartoonPage = async (props: any) => {
  const cartoonId = props?.params?.cartoonId || ''

  const cartoonUploads = await DbClient.init.table_manga_upload.find({
    cartoon_id: cartoonId,
  })

  let cartoonName = ''
  let projectName = ''

  const rawData = await cartoonUploads.toArray()

  const data = rawData.map((d): IMangaUpload => {
    if (!cartoonName) {
      cartoonName = d.cartoon_name
    }
    if (!projectName) {
      projectName = d.project_name
    }
    return {
      ...d,
      _id: d._id.toString(),
    }
  })
  return (
    <CartoonList
      data={data}
      cartoonId={cartoonId}
      cartoonName={cartoonName}
      projectName={projectName}
    />
  )
}

export default CartoonPage
