import React from 'react';
import styled from 'styled-components';

interface INavigationBar {

}

const Container = styled.nav`
    display: flex;
    flex-flow: row nowrap;
    flex: 1 1 100%;
    align-items: center;
    height: 100%;    
    margin: 0 auto;
    padding: 1.45rem 1.0875rem;
`;

export const NavigationBar = (props: INavigationBar) => {
    return (
        <Container>
            <div className="nav-item"><span>Home</span></div>
        </Container>
    )
}