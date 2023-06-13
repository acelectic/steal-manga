export const enum TriggerDownloadTypeEnum {
  MY_NOVEL = 'my-novel',
  MAN_MIRROR = 'man-mirror',
}
export interface ITriggerDownloadPayload {
  type: TriggerDownloadTypeEnum
}
