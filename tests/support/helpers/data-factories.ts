// Simple data factory following the data-factories pattern
// For generating unique, parallel-safe data

export const generateUniqueEmail = (prefix = 'user') => {
  return `${prefix}-${Date.now()}-${Math.floor(Math.random() * 10000)}@example.com`;
};

export const createUserData = (overrides = {}) => ({
  email: generateUniqueEmail(),
  password: 'TestPassword123!',
  first_name: 'Test',
  last_name: 'User',
  ...overrides,
});
