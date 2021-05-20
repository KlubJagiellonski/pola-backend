import styled from 'styled-components';
import {color} from './../styles/theme'

export const Wrapper = styled.div`
  background: ${color.black};
  color: ${color.white};
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  font-family: 'Roboto';
  font-size: 14px;
  font-weight: 700;
  min-height: 200px;
  padding: 35px 0;
  grid-area: download;

  @media only screen and (max-width: 768px) {
    min-height: 0;
  }
`;
