/**
 * Company Team Page - User Management in Company Settings
 * Company Settings → User Management
 * Placeholder: team management is available via the Team icon on the company card
 */

import { Users } from 'lucide-react'

export function CompanyTeamPage() {
  return (
    <div className="h-full flex flex-col items-center justify-center p-8 text-center">
      <Users className="w-16 h-16 text-gray-400 mb-4" />
      <h2 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
        User Management
      </h2>
      <p className="text-gray-500 dark:text-gray-400 max-w-sm mb-4">
        Manage team members and invitations. Use the Team icon on the company card to open the Team Management panel.
      </p>
      <p className="text-sm text-gray-400">
        A dedicated User Management page under Company Settings is coming soon.
      </p>
    </div>
  )
}
