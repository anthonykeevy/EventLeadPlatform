/**
 * KPI Modal Component
 * Story 2.6: Admin Public Event Review Workflow
 * 
 * Reusable modal for displaying KPI breakdowns with clickable counts
 */
import React from 'react'
import { X } from 'lucide-react'

export interface KPIBreakdown {
  label: string
  value: number
  color: string
  onClick?: () => void
}

interface KPIModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  totalLabel: string
  totalValue: number
  breakdowns: KPIBreakdown[]
  onTotalClick?: () => void
}

export const KPIModal: React.FC<KPIModalProps> = ({
  isOpen,
  onClose,
  title,
  totalLabel,
  totalValue,
  breakdowns,
  onTotalClick,
}) => {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div
          className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
          onClick={onClose}
        />

        {/* Modal panel */}
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          {/* Header */}
          <div className="bg-white px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-medium text-gray-900">{title}</h3>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-500 focus:outline-none"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="bg-white px-6 py-4">
            {/* Total */}
            <div className="mb-6">
              <div className="text-sm font-medium text-gray-500 mb-1">{totalLabel}</div>
              <button
                onClick={onTotalClick}
                className={`text-3xl font-bold ${
                  onTotalClick
                    ? 'text-teal-600 hover:text-teal-700 cursor-pointer transition-colors'
                    : 'text-gray-900 cursor-default'
                }`}
              >
                {totalValue}
              </button>
            </div>

            {/* Breakdowns */}
            <div className="grid grid-cols-3 gap-4">
              {breakdowns.map((breakdown, index) => (
                <div key={index} className="text-center">
                  <div className="text-xs font-medium text-gray-500 mb-2">{breakdown.label}</div>
                  <button
                    onClick={breakdown.onClick}
                    className={`text-2xl font-bold ${
                      breakdown.onClick
                        ? `${breakdown.color} hover:opacity-80 cursor-pointer transition-opacity`
                        : `${breakdown.color} cursor-default`
                    }`}
                  >
                    {breakdown.value}
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-6 py-3 border-t border-gray-200 flex justify-end">
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

