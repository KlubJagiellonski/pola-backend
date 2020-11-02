import React from 'react';
import {render, screen} from '@testing-library/react';
import SearchModal from "./SearchModal";


test('should display friends with scores', async () => {
    const {getByText, getByLabelText} = render(<SearchModal data={{
        name: "TEST-PRODUCT",
        plScore: 10,
        plCapital: 100,
        plWorkers: 100,
        plRnD: 100,
        plRegistered: 100,
        plNotGlobEnt: 100,
        is_friend: true,
        description: 'TEST-DESCRIPTION'
    }}/>);

    expect(screen.getByText('10 pkt')).toBeInTheDocument();

    expect(screen.getByText('udział polskiego kapitału 100 %')).toBeInTheDocument();
    expect(screen.getByTestId('pl-workers')).toHaveAttribute('checked', "")
    expect(screen.getByTestId('pl-rnd')).toHaveAttribute('checked', "")
    expect(screen.getByTestId('pl-registered')).toHaveAttribute('checked', "")
    expect(screen.getByTestId('pl-not-glob-ent')).toHaveAttribute('checked', "")

    expect(screen.getByText('To jest przyjaciel Poli')).toBeInTheDocument();
});

test('should without scores', async () => {
    const {getByText, getByLabelText} = render(<SearchModal data={{
        name: "TEST-PRODUCT",
        plScore: 10,
        plCapital: 0,
        plWorkers: 0,
        plRnD: 0,
        plRegistered: 0,
        plNotGlobEnt: 0,
        is_friend: true,
        description: 'TEST-DESCRIPTION'
    }}/>);

    expect(screen.getByText('10 pkt')).toBeInTheDocument();

    expect(screen.getByText('udział polskiego kapitału 0 %')).toBeInTheDocument();
    expect(screen.getByTestId('pl-workers')).not.toHaveAttribute('checked', "")
    expect(screen.getByTestId('pl-rnd')).not.toHaveAttribute('checked', "")
    expect(screen.getByTestId('pl-registered')).not.toHaveAttribute('checked', "")
    expect(screen.getByTestId('pl-not-glob-ent')).not.toHaveAttribute('checked', "")

    expect(screen.getByText('To jest przyjaciel Poli')).toBeInTheDocument();
    expect(screen.getByText('TEST-DESCRIPTION')).toBeInTheDocument();
});

test('should handle not-friends', async () => {
    const {container, getByText, getByLabelText} = render(<SearchModal data={{
        name: "TEST-PRODUCT",
        plScore: 20,
        plCapital: 0,
        plWorkers: 0,
        plRnD: 0,
        plRegistered: 0,
        plNotGlobEnt: 0,
        is_friend: false,
        description: 'TEST-DESCRIPTION'
    }}/>);

    expect(screen.getByText('20 pkt')).toBeInTheDocument();

    expect(container.textContent).not.toContain("To jest przyjaciel Poli")
});

test('should handle incorrect code', async () => {
    const {container, getByText, getByLabelText} = render(<SearchModal data={{
        name: "Nieprawidłowy kod",
        plScore: 20,
        plCapital: 0,
        plWorkers: 0,
        plRnD: 0,
        plRegistered: 0,
        plNotGlobEnt: 0,
        is_friend: false,
        description: 'TEST-DESCRIPTION'
    }}/>);

    expect(screen.queryByText('pkt')).not.toEqual();

    expect(screen.queryByText('udział polskiego kapitału 0 %')).not.toEqual();
    expect(screen.queryByTestId('pl-workers')).not.toEqual([])
    expect(screen.queryByTestId('pl-rnd')).not.toEqual([])
    expect(screen.queryByTestId('pl-registered')).not.toEqual([])
    expect(screen.queryByTestId('pl-not-glob-ent')).not.toEqual([])

    expect(screen.queryByText("To jest przyjaciel Poli")).not.toEqual([])
});
