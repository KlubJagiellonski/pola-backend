import styled from 'styled-components';
import { Button } from '../../styles/GlobalStyle.css';
import {Device} from './../../styles/theme'

export const Wrapper = styled.div`
  grid-area: articles;

  @media ${Device.mobile} {
    padding: 15px 30px;
    margin-bottom: 15px;
  }
`;

export const ArticlesButton = styled(Button)`
  margin-top: 10px;
`;
