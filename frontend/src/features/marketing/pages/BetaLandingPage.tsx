import { Link } from 'react-router-dom'
import { LandingHeroMock } from '../components/LandingHeroMock'
import { useLandingPageSeo } from '../hooks/useLandingPageSeo'

const VALUE_CHIPS = [
  'Branded forms',
  'Approval workflow',
  'Links, embeds, QR and kiosk capture',
] as const

const CAPABILITIES = [
  {
    title: 'Create branded forms quickly',
    body: 'Drag-and-drop form building with brand-friendly layouts and custom backgrounds your team can reuse.',
  },
  {
    title: 'Capture leads and feedback anywhere',
    body: 'Public links, website embeds, QR-friendly URLs and kiosk-style capture for events, sites and in-person interactions.',
  },
  {
    title: 'Manage approval before publishing',
    body: 'Let teams build while managers keep control over what goes live — with roles and audit history for governance.',
  },
  {
    title: 'Keep data useful after submission',
    body: 'Export responses and prepare for reporting and CRM handoff without spreadsheet handoffs.',
  },
  {
    title: 'Work across teams and companies',
    body: 'Multi-company workspaces, roles and sharing for branches, agencies and partners — with honest limits during Beta.',
  },
] as const

const USE_CASES = [
  { title: 'Event lead capture', benefit: 'Capture booth and event interest with branded forms.' },
  { title: 'Test-drive & demo requests', benefit: 'Qualify interest without rebuilding forms each campaign.' },
  { title: 'Registrations & RSVPs', benefit: 'Collect sign-ups with dates and activation windows.' },
  { title: 'Customer feedback & NPS', benefit: 'Structured feedback tied to events and campaigns.' },
  { title: 'Product inquiries', benefit: 'Route inquiries with fields your team actually uses.' },
  { title: 'Kiosk & reception capture', benefit: 'Tablet-friendly capture with reset-friendly public forms.' },
  { title: 'Agency & client campaign forms', benefit: 'Repeatable branded workspaces for client delivery.' },
] as const

const FAQ_ITEMS = [
  {
    question: 'What is EventLead?',
    answer:
      'EventLead is a customer engagement form platform for creating branded forms, capturing customer data, and managing the workflow around approvals, sharing and follow-up.',
  },
  {
    question: 'Who is EventLead for?',
    answer:
      'EventLead is for marketing teams, event teams, agencies and organisations that need to collect customer information through forms and manage what happens before and after submission.',
  },
  {
    question: 'What can I use EventLead for?',
    answer:
      'You can use EventLead for event lead capture, registrations, RSVPs, customer feedback, surveys, product inquiries, kiosk capture and campaign forms.',
  },
  {
    question: 'How is EventLead different from a generic form builder?',
    answer:
      'Generic form builders focus on collecting answers. EventLead focuses on the broader customer engagement workflow, including branding, approvals, team roles, sharing, event context and follow-up.',
  },
  {
    question: 'Is EventLead ready for production?',
    answer:
      'EventLead is currently in early Beta. Some capabilities are available now, and others are being validated with customers before production release. Please talk to Signal Platforms before production-critical workflows or sensitive data.',
  },
] as const

const CONTACT_EMAIL = 'support@eventlead.com'

export function BetaLandingPage() {
  useLandingPageSeo()

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:top-4 focus:left-4 focus:px-4 focus:py-2 focus:bg-white focus:rounded-md focus:shadow"
      >
        Skip to main content
      </a>

      <header className="border-b border-slate-200 bg-white/80 backdrop-blur sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between gap-4">
          <span className="text-lg font-bold text-teal-700">EventLead</span>
          <nav className="flex items-center gap-3 text-sm" aria-label="Account">
            <Link to="/login" className="text-slate-600 hover:text-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-500 rounded px-2 py-1">
              Log in
            </Link>
            <Link to="/signup" className="btn-primary text-sm whitespace-nowrap">
              Create an account
            </Link>
          </nav>
        </div>
      </header>

      <main id="main-content">
        {/* Hero */}
        <section className="bg-white border-b border-slate-100" aria-labelledby="hero-heading">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 lg:py-16 grid lg:grid-cols-2 gap-10 items-center">
            <div>
              <p className="text-sm font-medium text-teal-800 mb-4">
                Free Beta from Signal Platforms. Built for marketing, events and customer-engagement teams.
              </p>
              <h1 id="hero-heading" className="text-3xl sm:text-4xl font-bold text-slate-900 leading-tight mb-4">
                Build customer engagement forms your marketing team can actually use
              </h1>
              <p className="text-lg text-slate-600 mb-2">
                Create branded forms for events, campaigns and customer follow-up
              </p>
              <p className="text-slate-600 mb-6">
                EventLead helps teams build branded forms, capture customer data through links, embeds, QR codes or
                kiosks, and manage the workflow from approval to follow-up.
              </p>
              <div className="flex flex-col sm:flex-row gap-3 mb-4">
                <Link to="/signup" className="btn-primary text-center">
                  Create an account
                </Link>
                <a href="#example-forms" className="btn-outline text-center">
                  See example forms
                </a>
              </div>
              <p className="text-sm text-amber-900 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 mb-6">
                Early Beta: suitable for testing and pilots. Talk to us before using it for production-critical
                workflows.
              </p>
              <ul className="flex flex-wrap gap-2" aria-label="Quick value highlights">
                {VALUE_CHIPS.map((chip) => (
                  <li
                    key={chip}
                    className="text-xs font-medium px-3 py-1 rounded-full bg-teal-50 text-teal-900 border border-teal-100"
                  >
                    {chip}
                  </li>
                ))}
              </ul>
            </div>
            <LandingHeroMock />
          </div>
        </section>

        {/* Problem */}
        <section className="max-w-6xl mx-auto px-4 sm:px-6 py-14" aria-labelledby="problem-heading">
          <h2 id="problem-heading" className="text-2xl font-bold text-slate-900 mb-4">
            The form is only one part of the workflow
          </h2>
          <p className="text-slate-600 max-w-3xl mb-4">
            Most teams do not struggle because they cannot make a form. They struggle because the process around the
            form is messy: briefing, building, approving, publishing, collecting, exporting and following up.
          </p>
          <p className="text-slate-700 font-medium">EventLead is built for that whole workflow.</p>
          <ul className="mt-6 grid sm:grid-cols-2 gap-3 text-sm text-slate-600 list-disc list-inside">
            <li>Forms rebuilt from scratch for every campaign</li>
            <li>Waiting on developers, agencies or overloaded admins</li>
            <li>Lead data stuck in spreadsheets</li>
            <li>Manual brand checks and approvals</li>
            <li className="sm:col-span-2">Managers lack visibility across active forms and campaigns</li>
          </ul>
        </section>

        {/* Capabilities */}
        <section
          className="bg-white border-y border-slate-100 py-14"
          aria-labelledby="capabilities-heading"
        >
          <div className="max-w-6xl mx-auto px-4 sm:px-6">
            <h2 id="capabilities-heading" className="text-2xl font-bold text-slate-900 mb-2">
              Create branded forms without developer delays
            </h2>
            <p className="text-slate-600 mb-8 max-w-2xl">
              Hands-on teams get speed; managers and agencies get governance — on one platform.
            </p>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {CAPABILITIES.map((item) => (
                <article
                  key={item.title}
                  className="rounded-lg border border-slate-200 p-5 bg-slate-50/50 hover:border-teal-200 transition-colors"
                >
                  <h3 className="font-semibold text-slate-900 mb-2">{item.title}</h3>
                  <p className="text-sm text-slate-600">{item.body}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        {/* Platform lens */}
        <section className="max-w-6xl mx-auto px-4 sm:px-6 py-14" aria-labelledby="platform-heading">
          <h2 id="platform-heading" className="text-2xl font-bold text-slate-900 mb-4">
            Manage approvals, teams and follow-up
          </h2>
          <p className="text-slate-600 max-w-3xl">
            For marketing operations and enterprise-style teams: see forms and campaigns across workspaces, use
            approval before publish, and keep audit-friendly history — without claiming full enterprise compliance
            during Beta.
          </p>
        </section>

        {/* Differentiation */}
        <section
          className="bg-teal-900 text-white py-14"
          aria-labelledby="differentiation-heading"
        >
          <div className="max-w-6xl mx-auto px-4 sm:px-6">
            <h2 id="differentiation-heading" className="text-2xl font-bold mb-4">
              Why not just use a generic form tool?
            </h2>
            <p className="text-teal-50 max-w-3xl mb-8">
              Generic form tools help you collect answers. EventLead is designed around the workflow before and after
              the form: brand control, approval, sharing, event context, capture channels and follow-up visibility.
            </p>
            <dl className="grid sm:grid-cols-2 gap-6 text-sm">
              <div>
                <dt className="font-semibold text-teal-100">Generic forms</dt>
                <dd className="text-teal-50 mt-1">Quick data collection in isolation.</dd>
              </div>
              <div>
                <dt className="font-semibold text-white">EventLead</dt>
                <dd className="text-teal-50 mt-1">Governed customer engagement workflow.</dd>
              </div>
              <div>
                <dt className="font-semibold text-teal-100">Generic forms</dt>
                <dd className="text-teal-50 mt-1">Manual handoff to spreadsheets and CRM.</dd>
              </div>
              <div>
                <dt className="font-semibold text-white">EventLead</dt>
                <dd className="text-teal-50 mt-1">Forms connected to companies, events, permissions and export.</dd>
              </div>
            </dl>
          </div>
        </section>

        {/* Use cases / examples */}
        <section
          id="example-forms"
          className="max-w-6xl mx-auto px-4 sm:px-6 py-14 scroll-mt-20"
          aria-labelledby="use-cases-heading"
        >
          <h2 id="use-cases-heading" className="text-2xl font-bold text-slate-900 mb-2">
            Capture leads, registrations and feedback anywhere
          </h2>
          <p className="text-slate-600 mb-8">
            Example use cases you can build in EventLead — illustrated with safe mock content until public sample
            forms are published.
          </p>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {USE_CASES.map((uc) => (
              <article
                key={uc.title}
                className="rounded-lg border border-slate-200 p-4 bg-white shadow-sm"
              >
                <h3 className="font-semibold text-slate-900">{uc.title}</h3>
                <p className="text-sm text-slate-600 mt-1">{uc.benefit}</p>
              </article>
            ))}
          </div>
        </section>

        {/* FAQ */}
        <section
          className="bg-white border-t border-slate-100 py-14"
          aria-labelledby="faq-heading"
        >
          <div className="max-w-3xl mx-auto px-4 sm:px-6">
            <h2 id="faq-heading" className="text-2xl font-bold text-slate-900 mb-8">
              Frequently asked questions
            </h2>
            <dl className="space-y-6">
              {FAQ_ITEMS.map((item) => (
                <div key={item.question}>
                  <dt className="font-semibold text-slate-900">{item.question}</dt>
                  <dd className="mt-2 text-slate-600 text-sm leading-relaxed">{item.answer}</dd>
                </div>
              ))}
            </dl>
          </div>
        </section>

        {/* Final CTA */}
        <section
          className="max-w-6xl mx-auto px-4 sm:px-6 py-14 text-center"
          aria-labelledby="cta-heading"
        >
          <h2 id="cta-heading" className="text-2xl font-bold text-slate-900 mb-2">
            Start with a test account
          </h2>
          <p className="text-slate-600 mb-6 max-w-xl mx-auto">
            Ready to try it? Create your first branded form and see whether EventLead fits your team&apos;s workflow.
          </p>
          <Link to="/signup" className="btn-primary inline-block">
            Create an account
          </Link>
        </section>

        {/* Beta trust */}
        <section
          className="bg-amber-50 border-y border-amber-200 py-10"
          aria-labelledby="beta-heading"
        >
          <div className="max-w-3xl mx-auto px-4 sm:px-6 text-center">
            <h2 id="beta-heading" className="text-xl font-bold text-amber-950 mb-3">
              EventLead Beta
            </h2>
            <p className="text-amber-900 text-sm leading-relaxed">
              EventLead is currently in Beta. You can create an account and try it for free, but please talk to us
              before using it for production-critical workflows or sensitive data. If the Beta becomes useful for your
              team, we will work with you on the safest path to production when the platform is ready.
            </p>
          </div>
        </section>
      </main>

      <footer className="bg-slate-900 text-slate-300 py-10" role="contentinfo">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 text-sm space-y-4">
          <p className="font-semibold text-white">EventLead</p>
          <p>Signal Platforms Pty Ltd</p>
          <p>
            <a
              href={`mailto:${CONTACT_EMAIL}`}
              className="text-teal-300 hover:text-teal-200 underline focus:outline-none focus:ring-2 focus:ring-teal-400 rounded"
            >
              {CONTACT_EMAIL}
            </a>
          </p>
          <nav className="flex flex-wrap gap-x-4 gap-y-1" aria-label="Legal">
            <Link
              to="/privacy"
              className="text-teal-300 hover:text-teal-200 underline focus:outline-none focus:ring-2 focus:ring-teal-400 rounded"
            >
              Privacy Policy
            </Link>
            <Link
              to="/terms"
              className="text-teal-300 hover:text-teal-200 underline focus:outline-none focus:ring-2 focus:ring-teal-400 rounded"
            >
              Terms of Use
            </Link>
          </nav>
          <p className="text-slate-500 text-xs">Test / Beta environment — not for production-critical data.</p>
        </div>
      </footer>
    </div>
  )
}
