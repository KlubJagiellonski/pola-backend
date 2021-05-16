import styled from 'styled-components';
import { WrapperSection, TitleSection } from '../styles/GlobalStyle.css';
import {Device} from './../styles/theme'

export const Wrapper = styled(WrapperSection)`
  width: 100%;
  padding-top: 10px;
  padding-bottom: 30px;
  text-align: center;
  grid-area: friends;
  overflow: hidden;

  @media ${Device.mobile} {
    background-color: white;
    padding-top: 30px;
    padding-bottom: 40px;
  }
`;

type ImageProps = {
  amountElements: number;
};

export const ImageWrapper = styled.div`
  width: ${({ amountElements }: ImageProps) => (amountElements >= 10 ? '100' : amountElements + '0')}%;
  text-align: center;
`;

export const Title = styled(TitleSection)`
  @media ${Device.mobile} {
    font-size: 18px;
    margin-bottom: 20px;
  }
`;
