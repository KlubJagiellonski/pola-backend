import React from 'react';
import styled from 'styled-components';
import { color } from '../styles/theme';
import { PageSection } from './PageSection';

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 20rem;
`;

export const DevelopmentPlaceholder: React.FC = () => (
  <PageSection
    styles={{ backgroundColor: color.background.secondary, textColor: color.text.primary, textAlign: 'center' }}>
    <Container>
      <h2>Strona w budowie</h2>
    </Container>
  </PageSection>
);
