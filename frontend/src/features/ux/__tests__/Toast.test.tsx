import React from 'react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, act } from '@testing-library/react';
import { Toast, ToastContainer } from '../components/Toast';

describe('Toast', () => {
  const mockOnDismiss = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.runOnlyPendingTimers();
    vi.useRealTimers();
  });

  it('renders toast with message', () => {
    render(
      <Toast
        id="test-toast"
        type="success"
        message="Test message"
        onDismiss={mockOnDismiss}
      />
    );

    expect(screen.getByText('Test message')).toBeInTheDocument();
  });

  it('renders toast with title', () => {
    render(
      <Toast
        id="test-toast"
        type="success"
        title="Success"
        message="Test message"
        onDismiss={mockOnDismiss}
      />
    );

    expect(screen.getByText('Success')).toBeInTheDocument();
    expect(screen.getByText('Test message')).toBeInTheDocument();
  });

  it('renders different types with correct styling', () => {
    const { rerender } = render(
      <Toast
        id="test-toast"
        type="success"
        message="Success message"
        onDismiss={mockOnDismiss}
      />
    );

    expect(screen.getByRole('alert')).toHaveClass('bg-green-50', 'border-green-200');

    rerender(
      <Toast
        id="test-toast"
        type="error"
        message="Error message"
        onDismiss={mockOnDismiss}
      />
    );

    expect(screen.getByRole('alert')).toHaveClass('bg-red-50', 'border-red-200');

    rerender(
      <Toast
        id="test-toast"
        type="warning"
        message="Warning message"
        onDismiss={mockOnDismiss}
      />
    );

    expect(screen.getByRole('alert')).toHaveClass('bg-yellow-50', 'border-yellow-200');

    rerender(
      <Toast
        id="test-toast"
        type="info"
        message="Info message"
        onDismiss={mockOnDismiss}
      />
    );

    expect(screen.getByRole('alert')).toHaveClass('bg-blue-50', 'border-blue-200');
  });

  it('calls onDismiss when dismiss button is clicked', () => {
    render(
      <Toast
        id="test-toast"
        type="success"
        message="Test message"
        dismissible={true}
        onDismiss={mockOnDismiss}
      />
    );

    act(() => { vi.advanceTimersByTime(20); }); // Past entrance animation (10ms)

    const dismissButton = screen.getByRole('button', { name: /dismiss/i });
    fireEvent.click(dismissButton);

    act(() => { vi.advanceTimersByTime(350); }); // Past exit animation (300ms) before onDismiss fires

    expect(mockOnDismiss).toHaveBeenCalledWith('test-toast');
  });

  it('calls onRetry when retry button is clicked', () => {
    const mockOnRetry = vi.fn();

    render(
      <Toast
        id="test-toast"
        type="error"
        message="Test message"
        onDismiss={mockOnDismiss}
        onRetry={mockOnRetry}
      />
    );

    act(() => { vi.advanceTimersByTime(20); }); // Past entrance animation

    const retryButton = screen.getByRole('button', { name: /try again/i });
    fireEvent.click(retryButton);

    expect(mockOnRetry).toHaveBeenCalled();
  });

  it('auto-dismisses after duration', () => {
    render(
      <Toast
        id="test-toast"
        type="success"
        message="Test message"
        duration={1000}
        onDismiss={mockOnDismiss}
      />
    );

    expect(screen.getByText('Test message')).toBeInTheDocument();

    act(() => { vi.advanceTimersByTime(20); }); // Past entrance (10ms)
    act(() => { vi.advanceTimersByTime(1000); }); // Duration
    act(() => { vi.advanceTimersByTime(350); }); // Exit animation (300ms) before onDismiss

    expect(mockOnDismiss).toHaveBeenCalledWith('test-toast');
  });

  it('does not auto-dismiss when duration is 0', () => {
    render(
      <Toast
        id="test-toast"
        type="success"
        message="Test message"
        duration={0}
        onDismiss={mockOnDismiss}
      />
    );

    act(() => { vi.advanceTimersByTime(5000); });

    expect(mockOnDismiss).not.toHaveBeenCalled();
  });

  it('has correct ARIA attributes', () => {
    render(
      <Toast
        id="test-toast"
        type="success"
        message="Test message"
        onDismiss={mockOnDismiss}
        aria-live="assertive"
      />
    );

    act(() => { vi.advanceTimersByTime(20); }); // Past entrance animation

    const alert = screen.getByRole('alert');
    expect(alert).toHaveAttribute('aria-live', 'assertive');
    expect(alert).toHaveAttribute('aria-atomic', 'true');
  });
});

describe('ToastContainer', () => {
  const mockOnDismiss = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('renders nothing when no toasts', () => {
    const { container } = render(
      <ToastContainer
        toasts={[]}
        onDismiss={mockOnDismiss}
      />
    );

    expect(container.firstChild).toBeNull();
  });

  it('renders toasts in container', () => {
    const toasts = [
      {
        id: 'toast-1',
        type: 'success' as const,
        message: 'Success message',
        onDismiss: mockOnDismiss,
      },
      {
        id: 'toast-2',
        type: 'error' as const,
        message: 'Error message',
        onDismiss: mockOnDismiss,
      },
    ];

    render(
      <ToastContainer
        toasts={toasts}
        onDismiss={mockOnDismiss}
      />
    );

    expect(screen.getByText('Success message')).toBeInTheDocument();
    expect(screen.getByText('Error message')).toBeInTheDocument();
  });

  it('applies correct position classes', () => {
    const toasts = [
      {
        id: 'toast-1',
        type: 'success' as const,
        message: 'Test message',
        onDismiss: mockOnDismiss,
      },
    ];

    const { rerender } = render(
      <ToastContainer
        toasts={toasts}
        onDismiss={mockOnDismiss}
        position="top-right"
      />
    );

    const regionTopRight = screen.getByRole('region', { name: /notifications/i });
    expect(regionTopRight).toHaveClass('top-4', 'right-4');

    rerender(
      <ToastContainer
        toasts={toasts}
        onDismiss={mockOnDismiss}
        position="bottom-left"
      />
    );

    const regionBottomLeft = screen.getByRole('region', { name: /notifications/i });
    expect(regionBottomLeft).toHaveClass('bottom-4', 'left-4');
  });

  it('has correct ARIA attributes', () => {
    const toasts = [
      {
        id: 'toast-1',
        type: 'success' as const,
        message: 'Test message',
        onDismiss: mockOnDismiss,
      },
    ];

    render(
      <ToastContainer
        toasts={toasts}
        onDismiss={mockOnDismiss}
      />
    );

    const region = screen.getByRole('region', { name: /notifications/i });
    expect(region).toHaveAttribute('aria-live', 'polite');
    expect(region).toHaveAttribute('aria-label', 'Notifications');
  });
});

