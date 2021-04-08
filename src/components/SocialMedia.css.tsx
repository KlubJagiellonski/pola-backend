import styled from 'styled-components';
import { WrapperSection, TitleSection } from '../styles/GlobalStyle.css';

export const Wrapper = styled(WrapperSection)`
  padding: 40px 0;
  min-height: 120px;

  @media only screen and (min-width: 1900px) {
    min-height: 150px;
  }

  @media only screen and (min-width: 2500px) {
    min-height: 180px;
  }

  @media only screen and (max-width: 768px) {
    min-height: 0;
    padding: 30px 0;
  }
`;

export const Items = styled.div`
  align-items: center;
  justify-content: center;
  display: flex;
  flex-direction: row;
  width: 80%;
  float: left;

  @media only screen and (max-width: 768px) {
    width: 100%;
  }
`;

export const Item = styled.div`
  flex: 1;
  text-align: center;
`;

export const Title = styled(TitleSection)`
  width: 20%;
  float: left;
  text-align: center;
  margin: 0;

  @media only screen and (max-width: 768px) {
    width: 100%;
    margin-bottom: 20px;
    font-size: 18px;
  }
`;
