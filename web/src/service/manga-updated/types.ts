export interface IGetMangaUpdatedResponse {
  updated: string
  mangaExists: MangaExist[]
  manMirrorCartoons: ManMirrorCartoon[]
  myNovelCartoons: MyNovelCartoon[]
  resultsViewedSorted: [Date, ResultsViewedSortedClass[]][]
  resultsYetViewSorted: [Date, ResultsViewedSortedClass[]][]
}

export interface ResultsViewedSortedClass {
  projectName: Project
  projectDriveId: string
  cartoonId: string
  cartoonName: string
  cartoonDriveId: string
  mangaChapterName: string
  mangaChapterDriveId: string
  createdTime: string
  modifiedByMeTime: string
  viewedByMe: boolean
}

export enum Project {
  ManMirror = 'man-mirror',
  MyNovel = 'my-novel',
}

interface MangaConfig {
  cartoonName: string
  cartoonId: string
  latestChapter: number
  maxChapter: number
  disabled: boolean
  downloaded: number
  projectName: Project
  cartoonDriveId: string
}
export type ManMirrorCartoon = MangaConfig

export interface MangaExist {
  projectName: string
  mangaList: MangaList[]
}

export interface MangaList {
  mangaName: string
  total: number
}

export type MyNovelCartoon = MangaConfig

export interface IUpdateMangaConfigPayload {
  projectName: string
  cartoonName: string
  cartoonId: string
  latestChapter: number
  maxChapter: number
  disabled: boolean
  downloaded: number
}
