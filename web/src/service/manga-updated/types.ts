export interface IGetMangaUpdatedResponse {
  updated: string
  mangaExists: MangaExist[]
  manMirrorCartoons: ManMirrorCartoon[]
  myNovelCartoons: MyNovelCartoon[]
  resultsViewedSorted: [Date, ResultsViewedSortedClass[]][]
  resultsYetViewSorted: [Date, ResultsViewedSortedClass[]][]
}

export interface ResultsViewedSortedClass {
  projectName: EnumMangaProjectName
  projectDriveId: string
  cartoonId: string
  cartoonName: string
  cartoonDriveId: string
  mangaChapterName: string
  mangaChapterDriveId: string
  createdTime: string
  modifiedByMeTime: string
  viewedByMe: boolean
  latestSync: string
}

export enum EnumMangaProjectName {
  MAN_MIRROR = 'man-mirror',
  MY_NOVEL = 'my-novel',
}

export interface IMangaConfig {
  cartoonName: string
  cartoonId: string
  latestChapter: number
  maxChapter: number
  disabled: boolean
  downloaded: number
  projectName: EnumMangaProjectName
  cartoonDriveId: string
  latestSync?: string
}
export type ManMirrorCartoon = IMangaConfig

export interface MangaExist {
  projectName: string
  mangaList: MangaList[]
}

export interface MangaList {
  mangaName: string
  total: number
}

export type MyNovelCartoon = IMangaConfig

export type IUpdateMangaConfigPayload = IMangaConfig
