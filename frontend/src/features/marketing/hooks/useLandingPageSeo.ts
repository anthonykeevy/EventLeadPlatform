import { useEffect } from 'react'

const PAGE_TITLE = 'EventLead | Customer Engagement Forms'
const META_DESCRIPTION =
  'Build branded customer engagement forms for events, registrations, lead capture, surveys and feedback. Manage approvals, sharing and follow-up from one platform.'

const JSON_LD = [
  {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'EventLead',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Web',
    description:
      'Customer engagement form platform for creating branded forms, capturing customer data, and managing approvals, sharing and follow-up.',
    provider: {
      '@type': 'Organization',
      name: 'Signal Platforms Pty Ltd',
    },
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'AUD',
      description: 'Free during Beta — suitable for testing and pilots.',
    },
  },
  {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Signal Platforms Pty Ltd',
    url: typeof window !== 'undefined' ? window.location.origin : undefined,
  },
  {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: [
      {
        '@type': 'Question',
        name: 'What is EventLead?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'EventLead is a customer engagement form platform for creating branded forms, capturing customer data, and managing the workflow around approvals, sharing and follow-up.',
        },
      },
      {
        '@type': 'Question',
        name: 'Who is EventLead for?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'EventLead is for marketing teams, event teams, agencies and organisations that need to collect customer information through forms and manage what happens before and after submission.',
        },
      },
      {
        '@type': 'Question',
        name: 'What can I use EventLead for?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'You can use EventLead for event lead capture, registrations, RSVPs, customer feedback, surveys, product inquiries, kiosk capture and campaign forms.',
        },
      },
      {
        '@type': 'Question',
        name: 'How is EventLead different from a generic form builder?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Generic form builders focus on collecting answers. EventLead focuses on the broader customer engagement workflow, including branding, approvals, team roles, sharing, event context and follow-up.',
        },
      },
      {
        '@type': 'Question',
        name: 'Is EventLead ready for production?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'EventLead is currently in early Beta. Some capabilities are available now, and others are being validated with customers before production release. Talk to Signal Platforms before production-critical workflows or sensitive data.',
        },
      },
    ],
  },
]

function upsertMetaDescription(content: string) {
  let meta = document.querySelector('meta[name="description"]')
  if (!meta) {
    meta = document.createElement('meta')
    meta.setAttribute('name', 'description')
    document.head.appendChild(meta)
  }
  meta.setAttribute('content', content)
}

function upsertJsonLd(id: string, data: unknown) {
  let script = document.getElementById(id) as HTMLScriptElement | null
  if (!script) {
    script = document.createElement('script')
    script.id = id
    script.type = 'application/ld+json'
    document.head.appendChild(script)
  }
  script.textContent = JSON.stringify(data)
}

export function useLandingPageSeo() {
  useEffect(() => {
    const previousTitle = document.title
    upsertMetaDescription(META_DESCRIPTION)
    document.title = PAGE_TITLE
    JSON_LD.forEach((block, index) => {
      upsertJsonLd(`landing-jsonld-${index}`, block)
    })

    return () => {
      document.title = previousTitle
      JSON_LD.forEach((_, index) => {
        document.getElementById(`landing-jsonld-${index}`)?.remove()
      })
    }
  }, [])
}

export { PAGE_TITLE, META_DESCRIPTION }
