/**
 * Form Status Badge Component - Story 2.8
 * Displays form status and approval status badges
 */

import React from 'react'
import { FormStatus, FormApprovalStatus } from '../types/form.types'

interface FormStatusBadgeProps {
  status: FormStatus | null
  approvalStatus: FormApprovalStatus | null
}

export function FormStatusBadge({ status, approvalStatus }: FormStatusBadgeProps) {
  const getStatusColor = (statusCode: string | null): string => {
    if (!statusCode) return 'bg-gray-100 text-gray-800'
    
    switch (statusCode.toUpperCase()) {
      case 'DRAFT':
        return 'bg-yellow-100 text-yellow-800'
      case 'PUBLISHED':
        return 'bg-green-100 text-green-800'
      case 'ARCHIVED':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-blue-100 text-blue-800'
    }
  }

  const getApprovalColor = (approvalCode: string | null): string => {
    if (!approvalCode) return 'bg-gray-100 text-gray-800'
    
    switch (approvalCode.toUpperCase()) {
      case 'NO_APPROVAL':
        return 'bg-gray-100 text-gray-800'
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800'
      case 'APPROVED':
        return 'bg-green-100 text-green-800'
      case 'REJECTED':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-blue-100 text-blue-800'
    }
  }

  return (
    <div className="flex flex-col gap-1 items-end">
      {/* 
        Smart Status Display Logic:
        1. If Pending Approval -> Show "Pending Approval" (Orange) - Hide Draft
        2. If Rejected -> Show "Rejected" (Red) - Hide Draft
        3. If Approved but Draft -> Show "Ready to Publish" (Blue/Green) - Hide Draft
        4. Else -> Show Form Status (Draft, Published, Archived)
      */}
      
      {(() => {
        // Priority 1: Pending Approval
        if (approvalStatus?.approvalStatusCode?.toUpperCase() === 'PENDING') {
          return (
            <span className="px-2 py-1 text-xs font-medium rounded-full bg-orange-100 text-orange-800">
              Pending Approval
            </span>
          )
        }

        // Priority 2: Rejected
        if (approvalStatus?.approvalStatusCode?.toUpperCase() === 'REJECTED') {
          return (
            <span className="px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-800">
              Rejected
            </span>
          )
        }

        // Priority 3: Approved but not yet Published (Pre-approved)
        // Case-insensitive check to ensure we catch the pre-approval state
        if (approvalStatus?.approvalStatusCode?.toUpperCase() === 'APPROVED' && status?.statusCode?.toUpperCase() === 'DRAFT') {
          return (
            <span className="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
              Ready to Publish
            </span>
          )
        }

        // Priority 4: Default Form Status (Published, Archived, or Draft with No Approval needed)
        if (status) {
          return (
            <span
              className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(status.statusCode)}`}
              style={status.statusColor ? { backgroundColor: status.statusColor + '20', color: status.statusColor } : undefined}
            >
              {status.statusName}
            </span>
          )
        }

        return null
      })()}
    </div>
  )
}

