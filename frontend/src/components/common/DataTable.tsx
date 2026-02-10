/**
 * Reusable DataTable Component
 * Built with TanStack Table v8
 * Story 2.6: Admin Public Event Review Workflow
 * 
 * Features:
 * - Column definitions with sorting
 * - Client-side filtering
 * - Pagination
 * - Inline editing (optional)
 * - Expandable row forms (optional)
 * - Foreign key dropdowns
 * - Responsive design (mobile card view, desktop table view)
 * - Accessibility (keyboard navigation, ARIA labels)
 */

import { useState, useCallback, useEffect, useId, type ReactNode, Fragment } from 'react'
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  flexRender,
  type ColumnDef,
  type SortingState,
  type ColumnFiltersState,
  type Row,
} from '@tanstack/react-table'
import { ChevronDown, ChevronRight, ChevronUp, ChevronLeft, Search } from 'lucide-react'

export interface ColumnFilterConfig {
  columnId: string
  type: 'select' | 'text' | 'date'
  options?: Array<{ value: string | number; label: string }>
  placeholder?: string
  value?: string | number | null
}

export interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
  isLoading?: boolean
  enableSorting?: boolean
  enableFiltering?: boolean
  enablePagination?: boolean
  enableColumnFilters?: boolean
  columnFilterConfigs?: ColumnFilterConfig[]
  onColumnFilterChange?: (columnId: string, value: string | number | null) => void
  pageSize?: number
  currentPage?: number
  totalItems?: number
  pageSizeOptions?: number[]
  onPageChange?: (page: number) => void
  onPageSizeChange?: (pageSize: number) => void
  enableInlineEditing?: boolean
  enableExpandableRows?: boolean
  renderExpandedRow?: (row: Row<TData>) => ReactNode
  onRowEdit?: (row: Row<TData>, newData: Partial<TData>) => void
  onCellEdit?: (rowId: string, columnId: string, value: unknown) => void
  searchPlaceholder?: string
  emptyMessage?: string
}

export function DataTable<TData, TValue>({
  columns,
  data,
  isLoading = false,
  enableSorting = true,
  enableFiltering = true,
  enablePagination = true,
  enableColumnFilters = false,
  columnFilterConfigs = [],
  onColumnFilterChange,
  pageSize = 10,
  currentPage,
  totalItems,
  pageSizeOptions = [10, 20, 50],
  onPageChange,
  onPageSizeChange,
  enableInlineEditing: _enableInlineEditing = false,
  enableExpandableRows = false,
  renderExpandedRow,
  onRowEdit: _onRowEdit,
  onCellEdit: _onCellEdit,
  searchPlaceholder = 'Search...',
  emptyMessage = 'No data available',
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = useState<SortingState>([])
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
  const [globalFilter, setGlobalFilter] = useState('')
  const [expandedRows, setExpandedRows] = useState<Record<string, boolean>>({})
  const [_editingCell, _setEditingCell] = useState<{ rowId: string; columnId: string } | null>(null)
  const [internalPagination, setInternalPagination] = useState<{ pageIndex: number; pageSize: number }>({
    pageIndex: 0,
    pageSize,
  })
  const pageSizeSelectId = useId()

  const isControlledPagination = enablePagination && typeof currentPage === 'number' && typeof totalItems === 'number'

  const paginationState = isControlledPagination
    ? {
        pageIndex: Math.max(currentPage - 1, 0),
        pageSize: internalPagination.pageSize,
      }
    : internalPagination

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: enableSorting ? getSortedRowModel() : undefined,
    getFilteredRowModel: enableFiltering ? getFilteredRowModel() : undefined,
    getPaginationRowModel: enablePagination ? getPaginationRowModel() : undefined,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    globalFilterFn: 'includesString',
    initialState: {
      pagination: {
        pageSize,
      },
    },
    state: {
      sorting,
      columnFilters,
      globalFilter,
      pagination: paginationState,
    },
    manualPagination: isControlledPagination,
    pageCount:
      isControlledPagination && totalItems !== undefined && paginationState.pageSize > 0
        ? Math.max(1, Math.ceil(totalItems / paginationState.pageSize))
        : undefined,
    onPaginationChange: (updater) => {
      if (!enablePagination) {
        return
      }

      const nextValue =
        typeof updater === 'function'
          ? updater({
              pageIndex: paginationState.pageIndex,
              pageSize: paginationState.pageSize,
            })
          : updater

      if (isControlledPagination) {
        if (nextValue.pageSize !== paginationState.pageSize) {
          setInternalPagination((prev) => ({ ...prev, pageSize: nextValue.pageSize }))
          onPageSizeChange?.(nextValue.pageSize)
        }
        if (nextValue.pageIndex !== paginationState.pageIndex) {
          onPageChange?.(nextValue.pageIndex + 1)
        }
      } else {
        setInternalPagination(nextValue)
      }
    },
  })

  useEffect(() => {
    setInternalPagination((prev) => ({
      pageIndex: isControlledPagination && typeof currentPage === 'number' ? Math.max(currentPage - 1, 0) : prev.pageIndex,
      pageSize,
    }))
  }, [pageSize, isControlledPagination, currentPage])

  const toggleRowExpansion = useCallback((rowId: string) => {
    setExpandedRows((prev) => ({
      ...prev,
      [rowId]: !prev[rowId],
    }))
  }, [])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-teal-600"></div>
        <span className="ml-3 text-gray-600">Loading...</span>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Search/Filter Bar */}
      {enableFiltering && (
        <div className="flex items-center gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder={searchPlaceholder}
              value={globalFilter}
              onChange={(e) => setGlobalFilter(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              aria-label="Search table"
            />
          </div>
        </div>
      )}

      {/* Desktop Table View */}
      <div className="hidden md:block bg-white rounded-lg shadow border border-gray-200 w-full">
        <div className="overflow-x-auto w-full">
          <table className="min-w-full w-full divide-y divide-gray-200" role="table">
          <thead className="bg-gray-50">
            {table.getHeaderGroups().map((headerGroup) => (
              <tr key={headerGroup.id}>
                {enableExpandableRows && (
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-12">
                    <span className="sr-only">Expand</span>
                  </th>
                )}
                {headerGroup.headers.map((header) => (
                  <th
                    key={header.id}
                    className={`px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider ${
                      enableSorting && header.column.getCanSort() ? 'cursor-pointer hover:bg-gray-100' : ''
                    }`}
                    onClick={enableSorting ? header.column.getToggleSortingHandler() : undefined}
                  >
                    <div className="flex items-center gap-2">
                      {flexRender(header.column.columnDef.header, header.getContext())}
                      {enableSorting && header.column.getCanSort() && (
                        <span className="text-gray-400">
                          {{
                            asc: <ChevronUp className="w-4 h-4" />,
                            desc: <ChevronDown className="w-4 h-4" />,
                          }[header.column.getIsSorted() as string] ?? (
                            <div className="w-4 h-4" />
                          )}
                        </span>
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            ))}
            {enableColumnFilters && columnFilterConfigs.length > 0 && (
              <tr className="bg-gray-100 border-t border-gray-200">
                {enableExpandableRows && <th className="px-4 py-2 w-12"></th>}
                {table.getHeaderGroups()[0]?.headers.map((header) => {
                  const filterConfig = columnFilterConfigs.find((f) => f.columnId === header.id)
                  if (!filterConfig) {
                    return <th key={`filter-${header.id}`} className="px-4 py-2"></th>
                  }

                  return (
                    <th key={`filter-${header.id}`} className="px-4 py-2">
                      {filterConfig.type === 'select' && filterConfig.options ? (
                        <select
                          value={filterConfig.value || ''}
                          onChange={(e) => {
                            const value = e.target.value === '' ? null : (isNaN(Number(e.target.value)) ? e.target.value : Number(e.target.value))
                            onColumnFilterChange?.(header.id, value)
                          }}
                          className="w-full px-2 py-1 text-xs border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-teal-500 focus:border-teal-500 bg-white"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <option value="">All</option>
                          {filterConfig.options.map((option) => (
                            <option key={option.value} value={option.value}>
                              {option.label}
                            </option>
                          ))}
                        </select>
                      ) : filterConfig.type === 'text' ? (
                        <input
                          type="text"
                          placeholder={filterConfig.placeholder || 'Filter...'}
                          value={filterConfig.value || ''}
                          onChange={(e) => {
                            onColumnFilterChange?.(header.id, e.target.value || null)
                          }}
                          className="w-full px-2 py-1 text-xs border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-teal-500 focus:border-teal-500 bg-white"
                          onClick={(e) => e.stopPropagation()}
                        />
                      ) : null}
                    </th>
                  )
                })}
              </tr>
            )}
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {table.getRowModel().rows.length === 0 ? (
              <tr>
                <td
                  colSpan={columns.length + (enableExpandableRows ? 1 : 0)}
                  className="px-4 py-8 text-center text-gray-500"
                >
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              table.getRowModel().rows.map((row) => (
                <Fragment key={row.id}>
                  <tr className="hover:bg-gray-50 transition-colors">
                    {enableExpandableRows && (
                      <td className="px-4 py-3 whitespace-nowrap">
                        <button
                          onClick={() => toggleRowExpansion(row.id)}
                          className="p-1 rounded hover:bg-gray-200"
                          aria-label={expandedRows[row.id] ? 'Collapse row' : 'Expand row'}
                        >
                          {expandedRows[row.id] ? (
                            <ChevronDown className="w-4 h-4" />
                          ) : (
                            <ChevronRight className="w-4 h-4" />
                          )}
                        </button>
                      </td>
                    )}
                    {row.getVisibleCells().map((cell) => (
                      <td
                        key={cell.id}
                        className="px-4 py-3 whitespace-nowrap text-sm text-gray-900"
                      >
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </td>
                    ))}
                  </tr>
                  {enableExpandableRows && expandedRows[row.id] && renderExpandedRow && (
                    <tr>
                      <td colSpan={columns.length + 1} className="px-4 py-4 bg-gray-50">
                        {renderExpandedRow(row)}
                      </td>
                    </tr>
                  )}
                </Fragment>
              ))
            )}
          </tbody>
        </table>
        </div>
        
        {/* Pagination - Always at bottom of table container */}
        {enablePagination && (
          <div className="px-4 py-3 border-t border-gray-200">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              {/* Left: Rows per page */}
              <div className="flex items-center gap-2">
                <label className="text-sm text-gray-700" htmlFor={pageSizeSelectId}>
                  Rows per page
                </label>
                <select
                  id={pageSizeSelectId}
                  value={paginationState.pageSize}
                  onChange={(e) => {
                    const newSize = Number(e.target.value)
                    table.setPageSize(newSize)
                    if (isControlledPagination) {
                      onPageChange?.(1)
                    }
                  }}
                  className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                >
                  {pageSizeOptions.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>

              {/* Center: Page navigation */}
              <div className="flex items-center justify-center gap-2">
                <button
                  onClick={() => table.previousPage()}
                  disabled={!table.getCanPreviousPage()}
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  aria-label="Previous page"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <span className="text-sm text-gray-700 whitespace-nowrap">
                  Page {paginationState.pageIndex + 1} of {Math.max(table.getPageCount(), 1)}
                </span>
                <button
                  onClick={() => table.nextPage()}
                  disabled={!table.getCanNextPage()}
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  aria-label="Next page"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>

              {/* Right: Results count */}
              <div className="text-sm text-gray-700 text-center sm:text-right whitespace-nowrap">
                {isControlledPagination && totalItems !== undefined ? (
                  <>
                    Showing{' '}
                    {totalItems === 0
                      ? 0
                      : paginationState.pageIndex * paginationState.pageSize + 1}{' '}
                    –
                    {totalItems === 0
                      ? 0
                      : Math.min(
                          totalItems,
                          paginationState.pageIndex * paginationState.pageSize + data.length
                        )}{' '}
                    of {totalItems} results
                  </>
                ) : (
                  <>Showing {table.getRowModel().rows.length} of {data.length} results</>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Mobile Card View */}
      <div className="md:hidden space-y-4">
        {table.getRowModel().rows.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
            {emptyMessage}
          </div>
        ) : (
          <>
            {table.getRowModel().rows.map((row) => (
              <div key={row.id} className="bg-white rounded-lg shadow border border-gray-200 p-4">
                {enableExpandableRows && (
                  <button
                    onClick={() => toggleRowExpansion(row.id)}
                    className="mb-2 flex items-center gap-2 text-sm text-teal-600 hover:text-teal-700"
                  >
                    {expandedRows[row.id] ? (
                      <>
                        <ChevronDown className="w-4 h-4" /> Collapse
                      </>
                    ) : (
                      <>
                        <ChevronRight className="w-4 h-4" /> Expand
                      </>
                    )}
                  </button>
                )}
                <div className="space-y-2">
                  {row.getVisibleCells().map((cell) => (
                    <div key={cell.id} className="flex flex-col">
                      <span className="text-xs font-medium text-gray-500 uppercase">
                        {typeof cell.column.columnDef.header === 'string'
                          ? cell.column.columnDef.header
                          : cell.column.id}
                      </span>
                      <span className="text-sm text-gray-900">
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </span>
                    </div>
                  ))}
                </div>
                {enableExpandableRows && expandedRows[row.id] && renderExpandedRow && (
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    {renderExpandedRow(row)}
                  </div>
                )}
              </div>
            ))}
            
            {/* Mobile Pagination */}
            {enablePagination && (
              <div className="bg-white rounded-lg shadow border border-gray-200 px-4 py-3">
                <div className="flex flex-col gap-4">
                  {/* Rows per page */}
                  <div className="flex items-center justify-between">
                    <label className="text-sm text-gray-700" htmlFor={`${pageSizeSelectId}-mobile`}>
                      Rows per page
                    </label>
                    <select
                      id={`${pageSizeSelectId}-mobile`}
                      value={paginationState.pageSize}
                      onChange={(e) => {
                        const newSize = Number(e.target.value)
                        table.setPageSize(newSize)
                        if (isControlledPagination) {
                          onPageChange?.(1)
                        }
                      }}
                      className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-teal-500"
                    >
                      {pageSizeOptions.map((option) => (
                        <option key={option} value={option}>
                          {option}
                        </option>
                      ))}
                    </select>
                  </div>
                  
                  {/* Page navigation */}
                  <div className="flex items-center justify-between">
                    <button
                      onClick={() => table.previousPage()}
                      disabled={!table.getCanPreviousPage()}
                      className="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                      aria-label="Previous page"
                    >
                      <ChevronLeft className="w-4 h-4" />
                    </button>
                    <span className="text-sm text-gray-700">
                      Page {paginationState.pageIndex + 1} of {Math.max(table.getPageCount(), 1)}
                    </span>
                    <button
                      onClick={() => table.nextPage()}
                      disabled={!table.getCanNextPage()}
                      className="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                      aria-label="Next page"
                    >
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                  
                  {/* Results count */}
                  <div className="text-sm text-gray-700 text-center">
                    {isControlledPagination && totalItems !== undefined ? (
                      <>
                        Showing{' '}
                        {totalItems === 0
                          ? 0
                          : paginationState.pageIndex * paginationState.pageSize + 1}{' '}
                        –
                        {totalItems === 0
                          ? 0
                          : Math.min(
                              totalItems,
                              paginationState.pageIndex * paginationState.pageSize + data.length
                            )}{' '}
                        of {totalItems} results
                      </>
                    ) : (
                      <>Showing {table.getRowModel().rows.length} of {data.length} results</>
                    )}
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>

    </div>
  )
}
