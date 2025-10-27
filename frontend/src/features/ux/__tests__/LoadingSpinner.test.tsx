import React from 'react';
import { render, screen } from '@testing-library/react';
import { LoadingSpinner, ButtonLoadingSpinner, PageLoadingSpinner } from '../components/LoadingSpinner';

describe('LoadingSpinner', () => {
  it('renders with default props', () => {
    render(<LoadingSpinner />);

    const spinner = screen.getByRole('status');
    expect(spinner).toBeInTheDocument();
    expect(spinner).toHaveAttribute('aria-label', 'Loading');
  });

  it('renders with custom aria-label', () => {
    render(<LoadingSpinner aria-label="Custom loading" />);

    const spinner = screen.getByRole('status');
    expect(spinner).toHaveAttribute('aria-label', 'Custom loading');
  });

  it('renders with different sizes', () => {
    const { rerender } = render(<LoadingSpinner size="sm" />);
    expect(screen.getByRole('status')).toHaveClass('h-4', 'w-4');

    rerender(<LoadingSpinner size="md" />);
    expect(screen.getByRole('status')).toHaveClass('h-6', 'w-6');

    rerender(<LoadingSpinner size="lg" />);
    expect(screen.getByRole('status')).toHaveClass('h-8', 'w-8');

    rerender(<LoadingSpinner size="xl" />);
    expect(screen.getByRole('status')).toHaveClass('h-12', 'w-12');
  });

  it('renders with different colors', () => {
    const { rerender } = render(<LoadingSpinner color="primary" />);
    expect(screen.getByRole('status')).toHaveClass('text-blue-600');

    rerender(<LoadingSpinner color="secondary" />);
    expect(screen.getByRole('status')).toHaveClass('text-gray-600');

    rerender(<LoadingSpinner color="white" />);
    expect(screen.getByRole('status')).toHaveClass('text-white');

    rerender(<LoadingSpinner color="gray" />);
    expect(screen.getByRole('status')).toHaveClass('text-gray-400');
  });

  it('applies custom className', () => {
    render(<LoadingSpinner className="custom-class" />);

    const spinner = screen.getByRole('status');
    expect(spinner).toHaveClass('custom-class');
  });

  it('has screen reader text', () => {
    render(<LoadingSpinner />);

    expect(screen.getByText('Loading')).toBeInTheDocument();
    expect(screen.getByText('Loading')).toHaveClass('sr-only');
  });
});

describe('ButtonLoadingSpinner', () => {
  it('renders with correct props', () => {
    render(<ButtonLoadingSpinner />);

    const spinner = screen.getByRole('status');
    expect(spinner).toHaveClass('mr-2', 'h-4', 'w-4', 'text-white');
    expect(spinner).toHaveAttribute('aria-label', 'Loading');
  });

  it('applies custom className', () => {
    render(<ButtonLoadingSpinner className="custom-class" />);

    const spinner = screen.getByRole('status');
    expect(spinner).toHaveClass('custom-class');
  });
});

describe('PageLoadingSpinner', () => {
  it('renders with default message', () => {
    render(<PageLoadingSpinner />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renders with custom message', () => {
    render(<PageLoadingSpinner message="Please wait..." />);

    expect(screen.getByText('Please wait...')).toBeInTheDocument();
  });

  it('applies custom className', () => {
    render(<PageLoadingSpinner className="custom-class" />);

    const container = screen.getByText('Loading...').parentElement;
    expect(container).toHaveClass('custom-class');
  });

  it('has correct structure', () => {
    render(<PageLoadingSpinner />);

    const container = screen.getByText('Loading...').parentElement;
    expect(container).toHaveClass('flex', 'flex-col', 'items-center', 'justify-center', 'py-12');
  });
});

