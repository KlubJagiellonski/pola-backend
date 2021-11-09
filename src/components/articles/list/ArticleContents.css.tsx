import styled from 'styled-components';
import { Device, padding, color, fontSize } from '../../../styles/theme';
import { Text } from '../../../styles/GlobalStyle.css';

export const ArticleTag = styled.div`
  display: flex;
  justify-content: end;
  flex-direction: column;
  height: 100%;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  padding-bottom: ${padding.normal};

  @media ${Device.mobile} {
    display: none;
  }
`;

export const ArticleDate = styled(Text)`
  color: ${color.text.red};

  @media ${Device.mobile} {
    display: none;
  }
`;

export const ArticleText = styled(Text)`
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  font-size: ${fontSize.small};
`;
