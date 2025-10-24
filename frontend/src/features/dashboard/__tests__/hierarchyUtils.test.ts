/**
 * Hierarchy Utils Tests - Story 1.18
 * Tests for sliding window algorithm and hierarchy management
 */

import { describe, it, expect } from 'vitest'
import {
  getPathToCompany,
  calculateVisibleWindow,
  buildCompanyTree,
  flattenCompanyTree,
  findCompanyById
} from '../utils/hierarchyUtils'
import type { Company } from '../types/dashboard.types'

describe('hierarchyUtils', () => {
  const mockCompanies: Company[] = [
    {
      companyId: 1,
      companyName: 'Root Company',
      relationshipType: 'Head Office',
      userRole: 'Company Admin',
      parentCompanyId: null,
      childCompanies: [],
      eventCount: 5,
      formCount: 10,
      hierarchyLevel: 0,
      isPrimaryCompany: true
    },
    {
      companyId: 2,
      companyName: 'Child Company',
      relationshipType: 'Branch',
      userRole: 'Company User',
      parentCompanyId: 1,
      childCompanies: [],
      eventCount: 2,
      formCount: 3,
      hierarchyLevel: 1,
      isPrimaryCompany: false
    },
    {
      companyId: 3,
      companyName: 'Grandchild Company',
      relationshipType: 'Branch',
      userRole: 'Company User',
      parentCompanyId: 2,
      childCompanies: [],
      eventCount: 1,
      formCount: 1,
      hierarchyLevel: 2,
      isPrimaryCompany: false
    }
  ]

  describe('getPathToCompany', () => {
    it('should return path from root to target company', () => {
      const target = mockCompanies[2] // Grandchild
      const path = getPathToCompany(target, mockCompanies)
      
      expect(path).toHaveLength(3)
      expect(path[0].companyId).toBe(1) // Root
      expect(path[1].companyId).toBe(2) // Child
      expect(path[2].companyId).toBe(3) // Grandchild
    })

    it('should return single item for root company', () => {
      const target = mockCompanies[0] // Root
      const path = getPathToCompany(target, mockCompanies)
      
      expect(path).toHaveLength(1)
      expect(path[0].companyId).toBe(1)
    })
  })

  describe('calculateVisibleWindow - AC-1.18.2', () => {
    it('should show 5 levels max', () => {
      const target = mockCompanies[2]
      const result = calculateVisibleWindow(target, mockCompanies, 5)
      
      expect(result.visibleCompanyIds.length).toBeLessThanOrEqual(5)
    })

    it('should indicate more levels above/below when applicable', () => {
      // Create 10-level hierarchy
      const deepCompanies: Company[] = []
      for (let i = 0; i < 10; i++) {
        deepCompanies.push({
          companyId: i,
          companyName: `Level ${i}`,
          relationshipType: 'Branch',
          userRole: 'Company User',
          parentCompanyId: i > 0 ? i - 1 : null,
          childCompanies: [],
          eventCount: 0,
          formCount: 0,
          hierarchyLevel: i,
          isPrimaryCompany: i === 0
        })
      }
      
      const target = deepCompanies[5] // Middle of hierarchy
      const result = calculateVisibleWindow(target, deepCompanies, 5)
      
      expect(result.hasMoreAbove).toBe(true)
      expect(result.hasMoreBelow).toBe(true)
      expect(result.visibleCompanyIds).toHaveLength(5)
    })
  })

  describe('buildCompanyTree', () => {
    it('should build hierarchical tree from flat list', () => {
      const tree = buildCompanyTree(mockCompanies)
      
      expect(tree).toHaveLength(1) // One root
      expect(tree[0].companyId).toBe(1)
      expect(tree[0].childCompanies).toHaveLength(1)
      expect(tree[0].childCompanies[0].companyId).toBe(2)
    })
  })

  describe('findCompanyById', () => {
    it('should find company in tree', () => {
      const tree = buildCompanyTree(mockCompanies)
      const found = findCompanyById(tree, 2)
      
      expect(found).toBeDefined()
      expect(found?.companyName).toBe('Child Company')
    })

    it('should return undefined for non-existent company', () => {
      const tree = buildCompanyTree(mockCompanies)
      const found = findCompanyById(tree, 999)
      
      expect(found).toBeUndefined()
    })
  })
})



