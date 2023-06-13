export interface IGetMangaUpdatedResponse {
  updated: string
  mangaExists: MangaExist[]
  manMirrorCartoons: ManMirrorCartoon[]
  myNovelCartoons: MyNovelCartoon[]
  resultsViewedSorted: [Date, ResultsViewedSortedClass[]][]
  resultsYetViewSorted: [Date, ResultsViewedSortedClass[]][]
}

export interface ResultsViewedSortedClass {
  project: Project
  manga: string
  chapter: string
  viewedByMe: boolean
}

export enum Project {
  ManMirror = 'man-mirror',
  MyNovel = 'my-novel',
}

export interface ManMirrorCartoon {
  cartoonName: string
  cartoonId: string
  latestChapter: number
  maxChapter: string
  disabled: boolean
  downloaded: number
}

export interface MangaExist {
  projectName: string
  mangaList: MangaList[]
}

export interface MangaList {
  mangaName: string
  total: number
}

export interface MyNovelCartoon {
  cartoonName: string
  cartoonId: string
  latestChapter: number
  maxChapter: number
  disabled: boolean
  downloaded: number
}

export interface IUpdateMangaConfigPayload {
  projectName: string
  cartoonName: string
  cartoonId: string
  latestChapter: number
  maxChapter: number
  disabled: boolean
  downloaded: number
}
