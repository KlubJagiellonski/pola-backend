import styled from 'styled-components';
import { WrapperSection, TitleSection } from '../styles/GlobalStyle.css';

export const Wrapper = styled(WrapperSection)`
  padding-top: 10px;
  padding-bottom: 30px;
  text-align: center;
  margin-bottom: 15px;

  @media only screen and (max-width: 768px) {
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
  @media only screen and (max-width: 768px) {
    font-size: 18px;
    margin-bottom: 20px;
  }
`;
