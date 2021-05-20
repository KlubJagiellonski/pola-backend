import styled from 'styled-components';
import {Device, padding} from './../../styles/theme'
import {PrimaryButton } from '../buttons/PrimaryButton';

export const Wrapper = styled.div`
  grid-area: articles;

  @media ${Device.mobile} {
    padding: 15px 30px;
    margin-bottom: 15px;
  }
`;

export const ArticlesButton = styled(PrimaryButton)`
  width: 100%;
  padding: ${padding.normal}
`;
