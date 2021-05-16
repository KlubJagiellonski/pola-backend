import styled from 'styled-components';
import { WrapperSection, TitleSection, Button } from '../styles/GlobalStyle.css';

export const WrapperTeams = styled(WrapperSection)`
  height: 100%;
  min-height: 200px;
  margin-top: 15px;
  position: relative;
  padding: 0px;
  margin: 0px;

  @media only screen and (max-width: 768px) {
    background: none;
  }
`;

export const Wrapper = styled(WrapperTeams)`
  grid-area: teams;
`;

export const TextSection = styled.div`
  text-align: center;
  padding: 15px 100px 60px 100px;

  @media only screen and (max-width: 768px) {
    padding: 15px 50px 30px 50px;
  }
`;

export const Title = styled(TitleSection)`
  padding: 15px;
`;

export const ButtonTeams = styled(Button)`
  position: absolute;
  bottom: 0px;
  left: 0px;
  right: 0px;

  @media only screen and (max-width: 768px) {
    position: relative;
    margin-top: 20px;
  }
`;
