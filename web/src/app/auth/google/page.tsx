import to from 'await-to-js'
import { getAuthGoogleUrl } from '../../../service/auth'
import { AuthGoogle } from '../../../modules/auth/AuthGoogle'

const PageAuthGoogle = async () => {
  const [, data] = await to(getAuthGoogleUrl())
  return <AuthGoogle authorizationUrl={data?.authorizationUrl} />
}

export default PageAuthGoogle
