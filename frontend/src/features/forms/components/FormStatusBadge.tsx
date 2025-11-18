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
      {status && (
        <span
          className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(status.statusCode)}`}
          style={status.statusColor ? { backgroundColor: status.statusColor + '20', color: status.statusColor } : undefined}
        >
          {status.statusName}
        </span>
      )}
      {approvalStatus && approvalStatus.approvalStatusCode !== 'NO_APPROVAL' && (
        <span
          className={`px-2 py-1 text-xs font-medium rounded-full ${getApprovalColor(approvalStatus.approvalStatusCode)}`}
        >
          {approvalStatus.approvalStatusName}
        </span>
      )}
    </div>
  )
}

