import { Link } from 'react-router-dom'

const lastUpdated = '3 June 2026'

export function PrivacyPolicyPage() {
  return (
    <main className="min-h-screen bg-gray-50 px-4 py-8" role="main">
      <article className="mx-auto max-w-4xl rounded-lg bg-white p-6 shadow-lg sm:p-10">
        <Link to="/" className="text-sm font-medium text-teal-700 hover:underline">
          Back to EventLead
        </Link>

        <header className="mt-6 border-b border-gray-200 pb-6">
          <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">
            Beta privacy notice
          </p>
          <h1 className="mt-2 text-3xl font-bold text-gray-900 sm:text-4xl">
            Privacy Policy
          </h1>
          <p className="mt-3 text-sm text-gray-600">Last updated: {lastUpdated}</p>
          <p className="mt-4 text-gray-700">
            EventLead is currently in Beta. This notice explains how Signal Platforms Pty Ltd
            handles information collected through the EventLead test system.
          </p>
        </header>

        <div className="mt-8 space-y-8 text-gray-700">
          <section>
            <h2 className="text-xl font-semibold text-gray-900">Who operates EventLead?</h2>
            <p className="mt-3">
              EventLead is operated by Signal Platforms Pty Ltd. References to "we", "us" and
              "our" mean Signal Platforms Pty Ltd.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">Beta use and sensitive data</h2>
            <p className="mt-3">
              EventLead is provided for testing, discovery and pilot use while the product is still
              being validated. Please do not enter sensitive, regulated or production-critical data
              into the Beta unless we have agreed the use case with you in writing.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">Information we may collect</h2>
            <ul className="mt-3 list-disc space-y-2 pl-6">
              <li>Account information, such as name, email address and company details.</li>
              <li>Workspace and form content that you create while using the platform.</li>
              <li>Form submissions if you publish or test a form.</li>
              <li>Basic technical information such as browser, device, IP address and usage logs.</li>
              <li>Support or feedback information you choose to send us.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">How we use information</h2>
            <ul className="mt-3 list-disc space-y-2 pl-6">
              <li>To provide and improve the EventLead Beta.</li>
              <li>To support account access, authentication and platform security.</li>
              <li>To understand which workflows and features are useful during customer discovery.</li>
              <li>To troubleshoot issues, protect the service and respond to user requests.</li>
              <li>To contact you about your Beta use where appropriate.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">Sharing and disclosure</h2>
            <p className="mt-3">
              We do not sell your information. We may share information with service providers that
              help us operate the platform, comply with legal obligations, protect the service, or
              complete a request you make.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">Data retention and deletion</h2>
            <p className="mt-3">
              Because EventLead is in Beta, retention and deletion processes may change before
              production release. You can ask us to delete Beta account or test data where practical,
              subject to backups, audit needs and legal obligations.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">Production migration</h2>
            <p className="mt-3">
              If the Beta becomes useful for your team, contact us before relying on it for live
              operations. Any migration to a production environment will be discussed case by case
              and is not automatic.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">Contact</h2>
            <p className="mt-3">
              For privacy questions or Beta data requests, contact Signal Platforms Pty Ltd through
              your usual Signal Platforms contact or the support channel provided with your Beta
              access.
            </p>
          </section>
        </div>

        <footer className="mt-10 border-t border-gray-200 pt-6 text-sm text-gray-600">
          <p>
            This Beta privacy notice is a product notice, not legal advice. It should be reviewed
            before broad public launch.
          </p>
        </footer>
      </article>
    </main>
  )
}

export default PrivacyPolicyPage
