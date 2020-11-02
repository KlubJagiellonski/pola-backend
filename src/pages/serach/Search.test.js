import React from 'react';
import {render} from '@testing-library/react';
import Search from './Search';

import {fireEvent, waitForElement, screen} from '@testing-library/react'

test('renders search button', () => {
    const {getByText} = render(<Search/>);
    const button = getByText(/sprawdź/i);
    expect(button).toBeInTheDocument();
});

test('should handle polish products', async () => {
    const {getByText, getByLabelText} = render(<Search/>);

    fireEvent.input(getByLabelText(/Kod EAN/i), {
        target: {value: '590123123'}
    })

    fireEvent.click(getByText(/sprawdź/i))
    await waitForElement(() => screen.getByText('TEST-PRODUCT'))

    expect(screen.getByTestId('pl-workers')).toHaveAttribute('disabled', "")
});

test('should handle book', async () => {
    const {getByText, getByLabelText} = render(<Search/>);

    fireEvent.input(getByLabelText(/Kod EAN/i), {
        target: {value: '977123123'}
    })

    fireEvent.click(getByText(/sprawdź/i))
    await waitForElement(() => screen.getByText('Kod ISBN/ISSN/ISMN'))
});
