import { Link } from 'react-router-dom'

const lastUpdated = '3 June 2026'

export function TermsOfUsePage() {
  return (
    <main className="min-h-screen bg-gray-50 px-4 py-8" role="main">
      <article className="mx-auto max-w-4xl rounded-lg bg-white p-6 shadow-lg sm:p-10">
        <Link to="/" className="text-sm font-medium text-teal-700 hover:underline">
          Back to EventLead
        </Link>

        <header className="mt-6 border-b border-gray-200 pb-6">
          <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">
            Beta terms
          </p>
          <h1 className="mt-2 text-3xl font-bold text-gray-900 sm:text-4xl">
            Terms of Use
          </h1>
          <p className="mt-3 text-sm text-gray-600">Last updated: {lastUpdated}</p>
          <p className="mt-4 text-gray-700">
            These terms apply to use of the EventLead Beta test system operated by Signal
            Platforms Pty Ltd.
          </p>
        </header>

        <div className="mt-8 space-y-8 text-gray-700">
          <section>
            <h2 className="text-xl font-semibold text-gray-900">Beta service</h2>
            <p className="mt-3">
              EventLead is currently provided as a Beta for testing, pilots and feedback. Features
              may change, be unavailable, contain defects or be removed before production release.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">Free Beta access</h2>
            <p className="mt-3">
              EventLead is free to use during Beta unless we agree otherwise in writing. Free Beta
              access does not guarantee ongoing free access, production availability, migration,
              support levels or commercial terms after Beta.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">Acceptable use</h2>
            <ul className="mt-3 list-disc space-y-2 pl-6">
              <li>Use the Beta only for lawful testing, discovery or agreed pilot purposes.</li>
              <li>Do not upload malicious content, attempt to disrupt the service or bypass access controls.</li>
              <li>Do not use the Beta to process sensitive or production-critical data without written agreement.</li>
              <li>Do not misrepresent the Beta as a production-certified or compliance-certified service.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">User content and form data</h2>
            <p className="mt-3">
              You are responsible for the content you create, the forms you publish and the data you
              collect through the Beta. You should only collect information that you are authorised
              to collect and that is appropriate for a Beta environment.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">Availability and support</h2>
            <p className="mt-3">
              The Beta is provided without guaranteed uptime, support response times, data recovery
              commitments or production service levels. We may pause, change or end access to the
              Beta where needed.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">Production migration</h2>
            <p className="mt-3">
              If you start using EventLead seriously during Beta, let us know so we can work with
              you on the safest path to production when the platform is ready. Any migration support
              will be discussed case by case and is not automatic unless separately agreed.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">No warranties</h2>
            <p className="mt-3">
              To the extent permitted by law, the Beta is provided on an "as is" and "as available"
              basis. We do not promise that it will be uninterrupted, error-free or suitable for a
              specific production use case.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold text-gray-900">Contact</h2>
            <p className="mt-3">
              Questions about these Beta terms can be raised through your Signal Platforms contact
              or the support channel provided with your Beta access.
            </p>
          </section>
        </div>

        <footer className="mt-10 border-t border-gray-200 pt-6 text-sm text-gray-600">
          <p>
            These Beta terms are an interim product notice and should be reviewed before broad
            public launch.
          </p>
        </footer>
      </article>
    </main>
  )
}

export default TermsOfUsePage
