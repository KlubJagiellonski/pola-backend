import styled from 'styled-components';
import { WrapperSection } from '../styles/GlobalStyle.css';

export const Wrapper = styled(WrapperSection)`
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 50px;
  min-height: 410px;

  @media only screen and (min-width: 1900px) {
    min-height: 440px;
  }

  @media only screen and (min-width: 2500px) {
    min-height: 470px;
  }

  @media only screen and (max-width: 768px) {
    min-height: 200px;
  }
`;
