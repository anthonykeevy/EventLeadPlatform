/**
 * Hierarchy Utilities - Story 1.18
 * Sliding window algorithm for unlimited depth company hierarchy
 * AC-1.18.2: Unlimited hierarchy with 5-level sliding window display
 */

import type { Company } from '../types/dashboard.types'

const MAX_VISIBLE_LEVELS = 5

/**
 * Get full path from root to target company
 */
export function getPathToCompany(
  targetCompany: Company,
  allCompanies: Company[]
): Company[] {
  const path: Company[] = []
  let currentCompany: Company | undefined = targetCompany

  // Walk up hierarchy to root
  while (currentCompany) {
    path.unshift(currentCompany) // Add to beginning
    
    if (currentCompany.parentCompanyId) {
      currentCompany = allCompanies.find(c => c.companyId === currentCompany!.parentCompanyId)
    } else {
      break // Reached root
    }
  }

  return path
}

/**
 * Calculate visible window for sliding 5-level display
 * AC-1.18.2: 5-level sliding window
 */
export function calculateVisibleWindow(
  selectedCompany: Company,
  allCompanies: Company[],
  maxVisible: number = MAX_VISIBLE_LEVELS
): { visibleCompanyIds: number[]; fullPath: Company[]; hasMoreAbove: boolean; hasMoreBelow: boolean } {
  // Try to find the company with the longest path that goes through the selected company
  // This ensures we always get the full context of the tree up to the deepest leaf
  
  let longestPath: Company[] = [];
  
  // First, get path from root to selected company
  const pathToSelected = getPathToCompany(selectedCompany, allCompanies);
  longestPath = [...pathToSelected];
  
  // Find all possible paths that go through the selected company
  for (const company of allCompanies) {
    if (company.companyId !== selectedCompany.companyId) {
      const path = getPathToCompany(company, allCompanies);
      
      // Check if this path includes the selected company
      const selectedIndex = path.findIndex(c => c.companyId === selectedCompany.companyId);
      
      if (selectedIndex !== -1 && path.length > longestPath.length) {
        longestPath = path;
      }
    }
  }
  
  const fullPath = longestPath;
  
  // Find selected company index in the longest path
  const selectedIndex = fullPath.findIndex(c => c.companyId === selectedCompany.companyId)
  
  // Need to center window around selected item, but keep it within bounds
  const halfWindow = Math.floor(maxVisible / 2);
  
  let startIndex = Math.max(0, selectedIndex - halfWindow);
  let endIndex = Math.min(fullPath.length, startIndex + maxVisible);
  
  // If we're at the end, shift the start index back to show maxVisible items (if possible)
  if (endIndex - startIndex < maxVisible && fullPath.length >= maxVisible) {
    startIndex = endIndex - maxVisible;
  }
  
  // IMPORTANT FIX: Ensure endIndex is exact (so length is always maxVisible when possible)
  if (fullPath.length > maxVisible) {
    if (startIndex + maxVisible > fullPath.length) {
       startIndex = fullPath.length - maxVisible;
       endIndex = fullPath.length;
    } else {
       endIndex = startIndex + maxVisible;
    }
  } else {
    startIndex = 0;
    endIndex = fullPath.length;
  }
  
  const visibleWindow = fullPath.slice(startIndex, endIndex);
  
  return {
    visibleCompanyIds: visibleWindow.map(c => c.companyId),
    fullPath,
    hasMoreAbove: startIndex > 0,
    hasMoreBelow: endIndex < fullPath.length
  }
}

/**
 * Build hierarchical tree from flat company list
 */
export function buildCompanyTree(companies: Company[]): Company[] {
  const companyMap = new Map<number, Company>()
  const rootCompanies: Company[] = []

  // First pass: Create map and initialize childCompanies arrays
  companies.forEach(company => {
    companyMap.set(company.companyId, { ...company, childCompanies: [] })
  })

  // Second pass: Build parent-child relationships
  companies.forEach(company => {
    const companyNode = companyMap.get(company.companyId)!
    
    if (company.parentCompanyId) {
      const parent = companyMap.get(company.parentCompanyId)
      if (parent) {
        parent.childCompanies.push(companyNode)
      } else {
        // Orphaned company (parent not in user's companies) - treat as root
        rootCompanies.push(companyNode)
      }
    } else {
      // Root company (no parent)
      rootCompanies.push(companyNode)
    }
  })

  return rootCompanies
}

/**
 * Flatten company tree to array (depth-first)
 */
export function flattenCompanyTree(companies: Company[]): Company[] {
  const result: Company[] = []
  
  function traverse(company: Company, level: number = 0) {
    result.push({ ...company, hierarchyLevel: level })
    company.childCompanies.forEach(child => traverse(child, level + 1))
  }
  
  companies.forEach(company => traverse(company, 0))
  
  return result
}

/**
 * Find company by ID in hierarchy
 */
export function findCompanyById(companies: Company[], companyId: number): Company | undefined {
  for (const company of companies) {
    if (company.companyId === companyId) return company
    
    const found = findCompanyById(company.childCompanies, companyId)
    if (found) return found
  }
  
  return undefined
}




