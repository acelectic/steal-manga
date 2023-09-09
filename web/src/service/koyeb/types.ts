export interface IGetServiceResponse {
  service: IKoyebService
}

export enum EnumKoyebServiceStatus {
  STARTING = 'STARTING',
  HEALTHY = 'HEALTHY',
  DEGRADED = 'DEGRADED',
  UNHEALTHY = 'UNHEALTHY',
  DELETING = 'DELETING',
  DELETED = 'DELETED',
  PAUSING = 'PAUSING',
  PAUSED = 'PAUSED',
  RESUMING = 'RESUMING',
}

export interface IKoyebService {
  id: string
  createdAt: Date
  updatedAt: Date
  startedAt: Date
  succeededAt: Date
  pausedAt: null
  resumedAt: null
  terminatedAt: null
  name: string
  type: string
  organizationId: string
  appId: string
  status: EnumKoyebServiceStatus
  messages: string[]
  version: string
  activeDeploymentId: string
  latestDeploymentId: string
  state: State
}

export interface State {
  desiredDeployment: DesiredDeployment
  autoRelease: AutoRelease
}

export interface AutoRelease {
  groups: AutoReleaseGroup[]
}

export interface AutoReleaseGroup {
  name: string
  repository: string
  gitRef: string
  latestSha: string
}

export interface DesiredDeployment {
  groups: DesiredDeploymentGroup[]
}

export interface DesiredDeploymentGroup {
  name: string
  deploymentIds: string[]
}
