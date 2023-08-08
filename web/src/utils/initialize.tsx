'use client'

import dayjs from 'dayjs'
import 'dayjs/locale/th'
import customParseFormat from 'dayjs/plugin/customParseFormat'
import isSameOrAfter from 'dayjs/plugin/isSameOrAfter'
import timezone from 'dayjs/plugin/timezone'
import utc from 'dayjs/plugin/utc'

dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.locale('th')
dayjs.extend(customParseFormat)
dayjs.tz.setDefault('Asia/Bangkok')
dayjs.extend(isSameOrAfter)
