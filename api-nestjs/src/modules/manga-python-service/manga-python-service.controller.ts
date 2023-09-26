import { Controller } from '@nestjs/common'
import { MangaPythonService } from './manga-python-service.service'

@Controller('manga-python-service')
export class MangaPythonServiceController {
  constructor(private readonly mangaPythonServiceService: MangaPythonService) {}
}
