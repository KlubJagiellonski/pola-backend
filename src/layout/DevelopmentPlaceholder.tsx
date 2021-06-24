import React from 'react';
import styled from 'styled-components';
import { color } from '../styles/theme';
import { PageSection } from './PageSection';

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 12rem;
`;

interface IDevelopmentPlaceholder {
  text?: string;
}

export const DevelopmentPlaceholder: React.FC<IDevelopmentPlaceholder> = ({ text = 'Strona w budowie' }) => (
  <PageSection
    size="full"
    styles={{ backgroundColor: color.background.secondary, textColor: color.text.primary, textAlign: 'center' }}>
    <Container>
      <h2>{text}</h2>
    </Container>
  </PageSection>
);
