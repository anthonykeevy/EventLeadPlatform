import React from 'react'

type Props = {
  fallback: React.ReactNode
  children: React.ReactNode
}

type State = {
  hasError: boolean
}

export class ComponentErrorBoundary extends React.Component<Props, State> {
  state: State = { hasError: false }

  static getDerivedStateFromError(): State {
    return { hasError: true }
  }

  componentDidCatch(error: unknown) {
    // Keep non-fatal; surface in console for debugging.
    // eslint-disable-next-line no-console
    console.warn('Component render failed (non-fatal):', error)
  }

  render() {
    if (this.state.hasError) return this.props.fallback
    return this.props.children
  }
}

