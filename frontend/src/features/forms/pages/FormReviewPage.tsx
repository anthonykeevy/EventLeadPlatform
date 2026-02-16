/**
 * FormReviewPage - Story 5.6 placeholder, Story 5.7 full implementation
 * Review and Publish entry point - deep link target from admin queue.
 */
import { useParams, Link } from 'react-router-dom'

export function FormReviewPage() {
  const { formId } = useParams<{ formId: string }>()

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow p-6">
        <h1 className="text-xl font-bold text-gray-900 mb-2">Review and Publish</h1>
        <p className="text-gray-600 mb-4">
          Form ID: {formId}. Full review UI will be implemented in Story 5.7.
        </p>
        <Link
          to={`/forms/${formId}/builder`}
          className="text-teal-600 hover:underline"
        >
          Open in Builder →
        </Link>
      </div>
    </div>
  )
}
