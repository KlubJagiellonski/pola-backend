import React from 'react';
import { render } from '@testing-library/react';
import Modal from './Modal';
import { Route, Router } from 'react-router-dom';

import { withRouter } from '../../withRouter';
import { history } from '../../history'
import { fireEvent, waitFor } from '@testing-library/react'

const ModalWithRouter = withRouter(Modal)

test('should close modal page', () => {
  const { getByLabelText } = render(<ModalWithRouter />);

  fireEvent.click(getByLabelText(/Wyłącz/i));

  expect(history.location.pathname).toBe('/');
});

test('should handle data', async () => {
  history.push(`/ean/5900334005526`);

  const { getByText } = render(
    <Router history={history}>
      <Route path='/ean/:ean'>
        <Modal />
      </Route>
    </Router>
  );

  await waitFor(() =>
    getByText(/TEST-PRODUCT/i)
  )
});