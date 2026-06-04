import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { BetaLandingPage } from '../pages/BetaLandingPage'

function renderLanding() {
  return render(
    <MemoryRouter>
      <BetaLandingPage />
    </MemoryRouter>,
  )
}

describe('BetaLandingPage', () => {
  it('renders customer-facing H1 and primary CTA to signup', () => {
    renderLanding()

    expect(
      screen.getByRole('heading', {
        level: 1,
        name: /build customer engagement forms your marketing team can actually use/i,
      }),
    ).toBeInTheDocument()

    const signupLinks = screen.getAllByRole('link', { name: /create an account/i })
    expect(signupLinks.length).toBeGreaterThanOrEqual(1)
    expect(signupLinks[0]).toHaveAttribute('href', '/signup')
  })

  it('does not expose developer diagnostics', () => {
    renderLanding()

    expect(screen.queryByText(/development environment ready/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/backend api/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/swagger/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/mailhog/i)).not.toBeInTheDocument()
    expect(screen.queryByText(/fastapi/i)).not.toBeInTheDocument()
  })

  it('includes crawlable FAQ and beta trust wording', () => {
    renderLanding()

    expect(screen.getByText(/what is eventlead\?/i)).toBeInTheDocument()
    expect(screen.getAllByText(/early beta/i).length).toBeGreaterThan(0)
    expect(screen.getAllByText(/production-critical/i).length).toBeGreaterThan(0)
  })

  it('links secondary CTA to example forms section', () => {
    renderLanding()

    const examplesLink = screen.getByRole('link', { name: /see example forms/i })
    expect(examplesLink).toHaveAttribute('href', '#example-forms')
  })

  it('includes footer links to privacy and terms', () => {
    renderLanding()

    expect(screen.getByRole('link', { name: /privacy policy/i })).toHaveAttribute('href', '/privacy')
    expect(screen.getByRole('link', { name: /terms of use/i })).toHaveAttribute('href', '/terms')
  })
})
