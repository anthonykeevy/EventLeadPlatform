/**
 * KPI Card Component - Story 1.18
 * AC-1.18.8: KPI components display and update based on selected company
 */

import React from 'react'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface KPICardProps {
  label: string
  value: number | null
  icon: React.ReactNode
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
  isLoading?: boolean
  className?: string
}

export function KPICard({ 
  label, 
  value, 
  icon, 
  trend, 
  trendValue,
  isLoading = false,
  className = ''
}: KPICardProps) {
  if (isLoading) {
    return (
      <div className={`bg-white rounded-lg shadow p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="h-8 bg-gray-200 rounded w-3/4 mb-2"></div>
          <div className="h-3 bg-gray-200 rounded w-1/3"></div>
        </div>
      </div>
    )
  }

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-green-500" />
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-500" />
      case 'neutral':
        return <Minus className="w-4 h-4 text-gray-400" />
      default:
        return null
    }
  }

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return 'text-green-600'
      case 'down':
        return 'text-red-600'
      default:
        return 'text-gray-500'
    }
  }

  return (
    <div className={`bg-white rounded-lg shadow hover:shadow-md transition-shadow p-6 ${className}`}>
      {/* Icon and Label */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="text-teal-600">
            {icon}
          </div>
          <span className="text-sm font-medium text-gray-600">{label}</span>
        </div>
      </div>

      {/* Value */}
      <div className="mb-2">
        <span className="text-3xl font-bold text-gray-900">
          {value !== null ? value.toLocaleString() : '—'}
        </span>
      </div>

      {/* Trend (optional) */}
      {trend && trendValue && (
        <div className={`flex items-center gap-1 text-sm ${getTrendColor()}`}>
          {getTrendIcon()}
          <span>{trendValue}</span>
        </div>
      )}
    </div>
  )
}




