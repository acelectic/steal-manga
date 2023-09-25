import dayjs, { Dayjs } from 'dayjs'
import customParseFormat from 'dayjs/plugin/customParseFormat'
import isBetween from 'dayjs/plugin/isBetween'
import isLeapYear from 'dayjs/plugin/isLeapYear'
import isSameOrAfter from 'dayjs/plugin/isSameOrAfter'
import isSameOrBefore from 'dayjs/plugin/isSameOrBefore'
import isToday from 'dayjs/plugin/isToday'
import minMax from 'dayjs/plugin/minMax'
import objectSupport from 'dayjs/plugin/objectSupport'
import timezone from 'dayjs/plugin/timezone'
import toObject from 'dayjs/plugin/toObject'
import utc from 'dayjs/plugin/utc'
import numeral from 'numeral'

dayjs.extend(isBetween)
dayjs.extend(utc)
dayjs.extend(timezone)
dayjs.extend(customParseFormat)
dayjs.tz.setDefault('Asia/Bangkok')
dayjs.extend(isBetween)
dayjs.extend(isLeapYear)
dayjs.extend(isSameOrAfter)
dayjs.extend(isSameOrBefore)
dayjs.extend(isToday)
dayjs.extend(minMax)
dayjs.extend(objectSupport)
dayjs.extend(toObject)
dayjs.extend(customParseFormat)

declare global {
  interface String {
    toDayjs: (format?: string, strict?: boolean) => Dayjs
    toNumber: () => number
  }
  interface Date {
    toDayjs: (format?: string) => Dayjs
  }
  interface Number {
    toDayjs: (format?: string) => Dayjs
    format: (format: string) => string
  }
}

Date.prototype.toDayjs = function (format?: string) {
  return dayjs(this, format)
}

Number.prototype.toDayjs = function (format?: string) {
  return dayjs(this, format)
}

Number.prototype.format = function (format: string) {
  return numeral(this).format(format)
}

String.prototype.toDayjs = function (format?: string, strict?: boolean) {
  if (this === 'now') {
    return dayjs()
  }
  return dayjs(this as string, format, strict)
}

String.prototype.toNumber = function () {
  return numeral(this).value()
}
