import styled from 'styled-components';

import { WrapperSection, TitleSection } from '../styles/GlobalStyle.css';
import {Device, margin, padding} from '../styles/theme'
import {PrimaryButton } from './buttons/PrimaryButton';

export const WrapperTeams = styled(WrapperSection)`
  height: 100%;
  min-height: 11.4em;
  padding: ${margin.normal};
  position: relative;
  padding: 0px;
  margin: 0px;
`;

export const TextSection = styled.div`
  text-align: center;
  padding: ${padding.normal} ${padding.huge} ${padding.veryBig} ${padding.huge};

  @media ${Device.mobile} {
    padding: ${padding.normal} ${padding.big} ${padding.veryBig} ${padding.big};
  }
`;

export const Title = styled(TitleSection)`
  padding: ${padding.normal};
`;

export const ButtonTeams = styled(PrimaryButton)`
  position: absolute;
  bottom: 0px;
  left: 0px;
  right: 0px;
  width: 100%;
  padding: ${padding.normal};

  @media ${Device.mobile} {
    position: relative;
    margin-top: ${margin.normal}
  }
`;
