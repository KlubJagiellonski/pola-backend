import styled from 'styled-components';
import {Device, padding} from './../styles/theme'

export const Wrapper = styled.div`
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  overflow-x: hidden;
  padding-top: ${padding.normal};
  margin-bottom: -${padding.normal};
  display: grid;
  grid-gap: 15px;
  grid-template-areas:
     "articles development"
     "articles social-media"
     "articles about"
     "friends friends"
     "teams-friend teams"
     "download download";

  @media ${Device.mobile} {
    margin: 0;
    padding: 0;
    grid-gap: 0px;
    grid-template-areas:
     "development"
     "articles"
     "about"
     "social-media"
     "friends"
     "teams-friend"
     "teams"
     "download";
  }
`;
