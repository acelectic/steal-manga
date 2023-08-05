export const enum TriggerDownloadTypeEnum {
  MY_NOVEL = 'my-novel',
  MAN_MIRROR = 'man-mirror',
}
export interface ITriggerDownloadPayload {
  types: TriggerDownloadTypeEnum[]
}

export interface IDownloadMangaOnePayload {
  projectName: string
  cartoonName: string
  cartoonId: string
  latestChapter: number
  maxChapter: number
  disabled: boolean
  downloaded: number
}
