import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { EnhancedFormInput } from '../components/EnhancedFormInput';

describe('EnhancedFormInput', () => {
  const defaultProps = {
    label: 'Test Label',
    name: 'test',
    value: '',
    onChange: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders with label', () => {
    render(<EnhancedFormInput {...defaultProps} />);

    expect(screen.getByText('Test Label')).toBeInTheDocument();
    expect(screen.getByLabelText('Test Label')).toBeInTheDocument();
  });

  it('renders as text input by default', () => {
    render(<EnhancedFormInput {...defaultProps} />);

    const input = screen.getByRole('textbox');
    expect(input).toHaveAttribute('type', 'text');
  });

  it('renders as different input types', () => {
    const { rerender } = render(<EnhancedFormInput {...defaultProps} type="email" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'email');

    rerender(<EnhancedFormInput {...defaultProps} type="password" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'password');

    rerender(<EnhancedFormInput {...defaultProps} type="tel" />);
    expect(screen.getByRole('textbox')).toHaveAttribute('type', 'tel');
  });

  it('renders as textarea when type is textarea', () => {
    render(<EnhancedFormInput {...defaultProps} type="textarea" />);

    const textarea = screen.getByRole('textbox');
    expect(textarea.tagName).toBe('TEXTAREA');
  });

  it('calls onChange when value changes', async () => {
    const user = userEvent.setup();
    const onChange = jest.fn();

    render(<EnhancedFormInput {...defaultProps} onChange={onChange} />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'test value');

    expect(onChange).toHaveBeenCalledWith('test value');
  });

  it('shows error message when error prop is provided', () => {
    render(<EnhancedFormInput {...defaultProps} error="This field is required" />);

    expect(screen.getByText('This field is required')).toBeInTheDocument();
    expect(screen.getByRole('textbox')).toHaveAttribute('aria-invalid', 'true');
  });

  it('shows success state when success prop is true', () => {
    render(<EnhancedFormInput {...defaultProps} success={true} />);

    expect(screen.getByText('Looks good!')).toBeInTheDocument();
    expect(screen.getByRole('textbox')).toHaveClass('border-green-300');
  });

  it('shows required indicator when required prop is true', () => {
    render(<EnhancedFormInput {...defaultProps} required={true} />);

    expect(screen.getByText('*')).toBeInTheDocument();
    expect(screen.getByRole('textbox')).toHaveAttribute('required');
  });

  it('shows character count when showCharacterCount is true and maxLength is provided', () => {
    render(
      <EnhancedFormInput
        {...defaultProps}
        value="test"
        showCharacterCount={true}
        maxLength={10}
      />
    );

    expect(screen.getByText('4/10 characters')).toBeInTheDocument();
  });

  it('shows password toggle when showPasswordToggle is true and type is password', () => {
    render(
      <EnhancedFormInput
        {...defaultProps}
        type="password"
        showPasswordToggle={true}
      />
    );

    const toggleButton = screen.getByRole('button', { name: /show password/i });
    expect(toggleButton).toBeInTheDocument();
  });

  it('toggles password visibility when toggle button is clicked', async () => {
    const user = userEvent.setup();

    render(
      <EnhancedFormInput
        {...defaultProps}
        type="password"
        showPasswordToggle={true}
      />
    );

    const input = screen.getByRole('textbox');
    const toggleButton = screen.getByRole('button', { name: /show password/i });

    expect(input).toHaveAttribute('type', 'password');

    await user.click(toggleButton);
    expect(input).toHaveAttribute('type', 'text');
    expect(toggleButton).toHaveAttribute('aria-label', 'Hide password');

    await user.click(toggleButton);
    expect(input).toHaveAttribute('type', 'password');
    expect(toggleButton).toHaveAttribute('aria-label', 'Show password');
  });

  it('shows clear button when showClearButton is true and has value', () => {
    render(
      <EnhancedFormInput
        {...defaultProps}
        value="test value"
        showClearButton={true}
      />
    );

    const clearButton = screen.getByRole('button', { name: /clear input/i });
    expect(clearButton).toBeInTheDocument();
  });

  it('clears input when clear button is clicked', async () => {
    const user = userEvent.setup();
    const onChange = jest.fn();

    render(
      <EnhancedFormInput
        {...defaultProps}
        value="test value"
        showClearButton={true}
        onChange={onChange}
      />
    );

    const clearButton = screen.getByRole('button', { name: /clear input/i });
    await user.click(clearButton);

    expect(onChange).toHaveBeenCalledWith('');
  });

  it('shows floating label when floatingLabel is true', () => {
    render(<EnhancedFormInput {...defaultProps} floatingLabel={true} />);

    const label = screen.getByText('Test Label');
    expect(label).toHaveClass('absolute', 'left-3');
  });

  it('shows regular label when floatingLabel is false', () => {
    render(<EnhancedFormInput {...defaultProps} floatingLabel={false} />);

    const label = screen.getByText('Test Label');
    expect(label).toHaveClass('block', 'text-sm', 'font-medium');
  });

  it('calls onBlur when input loses focus', async () => {
    const user = userEvent.setup();
    const onBlur = jest.fn();

    render(<EnhancedFormInput {...defaultProps} onBlur={onBlur} />);

    const input = screen.getByRole('textbox');
    await user.click(input);
    await user.tab();

    expect(onBlur).toHaveBeenCalled();
  });

  it('applies disabled state correctly', () => {
    render(<EnhancedFormInput {...defaultProps} disabled={true} />);

    const input = screen.getByRole('textbox');
    expect(input).toBeDisabled();
    expect(input).toHaveClass('disabled:bg-gray-50', 'disabled:text-gray-500');
  });

  it('applies custom className', () => {
    render(<EnhancedFormInput {...defaultProps} className="custom-class" />);

    const container = screen.getByText('Test Label').closest('div');
    expect(container).toHaveClass('custom-class');
  });

  it('applies custom input className', () => {
    render(<EnhancedFormInput {...defaultProps} inputClassName="custom-input-class" />);

    const input = screen.getByRole('textbox');
    expect(input).toHaveClass('custom-input-class');
  });

  it('has correct ARIA attributes', () => {
    render(
      <EnhancedFormInput
        {...defaultProps}
        error="Test error"
        aria-describedby="test-description"
      />
    );

    const input = screen.getByRole('textbox');
    expect(input).toHaveAttribute('aria-invalid', 'true');
    expect(input).toHaveAttribute('aria-describedby', 'error-test test-description');
  });
});

