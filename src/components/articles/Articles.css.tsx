import styled from 'styled-components';
import { Button } from '../../styles/GlobalStyle.css';

export const Wrapper = styled.div`
  @media only screen and (max-width: 768px) {
    padding: 15px 30px;
    margin-bottom: 15px;
  }
`;

export const ArticlesButton = styled(Button)`
  margin-top: 10px;
`;
