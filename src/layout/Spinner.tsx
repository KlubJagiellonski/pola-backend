import React from 'react';
import Loader from 'react-loader-spinner';
import styled from 'styled-components';
import { seconds } from '../domain/generic';
import { color, pixels } from '../styles/theme';

const Container = styled.div`
  display: flex;
  flex-flow: column;
  text-align: center;
`;

interface ISpinner {
  text?: string;
  timeout?: seconds;
  styles?: {
    size?: pixels;
    color?: string;
  };
}

export const Spinner: React.FC<ISpinner> = ({ text, timeout, styles = { size: 80, color: color.button.red } }) => (
  <Container>
    <Loader type="Rings" color={styles.color} height={styles.size} width={styles.size} timeout={timeout} />
    {text && <label>{text}</label>}
  </Container>
);
