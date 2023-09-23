export const openGoogleDrive = (driveId: string) => {
  const googleDriveLink = `https://drive.google.com/drive/u/0/folders/${driveId}`
  window.open(googleDriveLink, '_blank')
}
