import styled from 'styled-components';
import { WrapperSection } from '../../styles/GlobalStyle.css';

export const Wrapper = styled(WrapperSection)`
  display: flex;
  flex-direction: row;
  min-height: 220px;
  margin-bottom: 15px;

  @media only screen and (min-width: 1900px) {
    min-height: 250px;
  }

  @media only screen and (min-width: 2500px) {
    min-height: 280px;
  }

  @media only screen and (max-width: 768px) {
    background-color: white;
    min-height: 120px;
  }
`;

export const ArticleImage = styled.div<{img?: string;}>`
  width: 50%;
  height: auto;
  text-align: left;
  /* background: url(${({ img }) => img});
  background-repeat: no-repeat;
  background-size: cover; */

  @media only screen and (max-width: 768px) {
    width: 40%;
    background-size: contain;
    background-position: center;
  }
`;

export const ArticleSection = styled.div`
  width: 50%;
  margin: 0 15px;

  @media only screen and (max-width: 768px) {
    width: 60%;
  }
`;

export const ArticleButton = styled.button`
  font-family: 'Roboto';
  font-size: 12px;
  font-weight: 300;
  margin-top: 40px;
  margin-bottom: 15px;
  background: #c4c4c4;
  border-radius: 3px;
  padding: 5px 10px;
  cursor: pointer;
  border: none;
`;
