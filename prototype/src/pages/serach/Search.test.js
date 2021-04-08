import React from 'react';
import { render } from '@testing-library/react';
import Search from './Search';

import { withRouter } from '../../withRouter';
import { history } from '../../history'
import { fireEvent } from '@testing-library/react'

const SearchWithRouter = withRouter(Search)

test('renders search button', () => {
  const { getByLabelText } = render(<Search />);

  const button = getByLabelText(/wyszukaj/i);

  expect(button).toBeInTheDocument();
});

test('should handle polish products', async () => {
  const { getByLabelText, getByTestId } = render(<SearchWithRouter />);

  fireEvent.input(getByLabelText(/Kod EAN/i), {
    target: { value: '590123123' }
  })

  fireEvent.submit(getByTestId(/form/i))
  expect(history.location.pathname).toBe('/ean/590123123');
});