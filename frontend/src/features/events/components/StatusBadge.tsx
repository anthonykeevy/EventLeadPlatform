/**
 * Status Badge Component - Story 2.4 Task 7
 * Displays event status with color coding
 */

import React from 'react'
import { EventStatus } from '../types/events.types'

interface StatusBadgeProps {
  status: EventStatus | null
  className?: string
}

export function StatusBadge({ status, className = '' }: StatusBadgeProps) {
  if (!status) {
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 ${className}`}>
        Unknown
      </span>
    )
  }

  // Use status color from backend if available, otherwise default based on status code
  const getStatusStyles = (): string => {
    if (status.statusColor) {
      // Use backend-provided color (format: #RRGGBB)
      const hexColor = status.statusColor.replace('#', '')
      return `bg-[#${hexColor}]20 text-[#${hexColor}] border border-[#${hexColor}]40`
    }

    // Fallback colors based on common status codes
    const code = status.statusCode.toLowerCase()
    if (code.includes('draft')) {
      return 'bg-gray-100 text-gray-800 border border-gray-300'
    }
    if (code.includes('published') || code.includes('live')) {
      return 'bg-green-100 text-green-800 border border-green-300'
    }
    if (code.includes('completed')) {
      return 'bg-blue-100 text-blue-800 border border-blue-300'
    }
    if (code.includes('cancelled')) {
      return 'bg-red-100 text-red-800 border border-red-300'
    }
    if (code.includes('pending')) {
      return 'bg-yellow-100 text-yellow-800 border border-yellow-300'
    }

    // Default
    return 'bg-teal-100 text-teal-800 border border-teal-300'
  }

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusStyles()} ${className}`}
      title={status.statusDescription || status.statusName}
    >
      {status.statusIcon && <span className="mr-1">{status.statusIcon}</span>}
      {status.statusName}
    </span>
  )
}
