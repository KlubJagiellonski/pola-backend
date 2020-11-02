import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

test('renders search button', () => {
  const { getByText } = render(<App />);
  const button = getByText(/sprawdź/i);
  expect(button).toBeInTheDocument();
});
