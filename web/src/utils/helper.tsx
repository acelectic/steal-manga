export const openGoogleDrive = (driveId: string) => {
  const googleDriveLink = makeGoogleDriveLink(driveId)
  window.open(googleDriveLink, '_blank')
}

export const makeGoogleDriveLink = (driveId: string) => {
  return `https://drive.google.com/drive/u/0/folders/${driveId}`
}

export const openLink = (link: string, newTab = true) => {
  window.open(link, newTab ? '_blank' : '_self')
}
