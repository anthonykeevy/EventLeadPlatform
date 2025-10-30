/**
 * Profile Features for Epic 2 Story 2.1
 * User Profile Enhancement Components and API
 */

// Components
export { ProfileEditor } from './components/ProfileEditor'
export { IndustryManager } from './components/IndustryManager'

// API
export * as usersApi from './api/usersApi'

// Types
export type {
  EnhancedUserProfile,
  ProfileUpdateRequest,
  ProfileUpdateResponse,
  IndustryAssociation,
  IndustryAssociationRequest,
  ReferenceOption
} from './types/profile.types'

