import styled from 'styled-components';
import { WrapperSection } from '../styles/GlobalStyle.css';
import {Device} from './../styles/theme'

export const Wrapper = styled(WrapperSection)`
  display: flex;
  flex-direction: row;
  min-height: 190px;
  grid-area: development;

  @media only screen and (min-width: 1900px) {
    min-height: 220px;
  }

  @media only screen and (min-width: 2500px) {
    min-height: 250px;
  }

  @media ${Device.mobile} {
    min-height: 150px;
  }
`;

type ImageProps = {
  img: string;
};

export const Image = styled.div`
  width: 50%;
  height: auto;
  text-align: left;
  background: url(${({ img }: ImageProps) => img});
  background-repeat: no-repeat;
  background-size: cover;
  border: 1px solid grey;
`;

export const TextSection = styled.div`
  margin: 0 15px;
  width: 50%;
`;
