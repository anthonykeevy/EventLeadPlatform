/**
 * KPI Section Component - Story 1.18
 * AC-1.18.8: KPI component area at top of dashboard
 */

import React from 'react'
import { FileText, Users as UsersIcon, Calendar } from 'lucide-react'
import { KPICard } from './KPICard'
import type { KPIData } from '../types/dashboard.types'

interface KPISectionProps {
  kpiData: KPIData | null
  isLoading: boolean
}

export function KPISection({ kpiData, isLoading }: KPISectionProps) {
  return (
    <div className="mb-8">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Overview</h2>
      
      {/* KPI Cards Grid - AC-1.18.11: Responsive (3 cols desktop, 2 tablet, 1 mobile) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <KPICard
          label="Total Forms"
          value={kpiData?.totalForms ?? null}
          icon={<FileText className="w-6 h-6" />}
          isLoading={isLoading}
        />
        
        <KPICard
          label="Total Leads"
          value={kpiData?.totalLeads ?? null}
          icon={<UsersIcon className="w-6 h-6" />}
          isLoading={isLoading}
        />
        
        <KPICard
          label="Active Events"
          value={kpiData?.activeEvents ?? null}
          icon={<Calendar className="w-6 h-6" />}
          isLoading={isLoading}
        />
      </div>
    </div>
  )
}



