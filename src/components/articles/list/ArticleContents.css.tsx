import styled from "styled-components";
import { Device, margin, color, fontSize } from "../../../styles/theme";
import { Text } from '../../../styles/GlobalStyle.css';

export const ArticleTag = styled.div`
  @media ${Device.desktop} {
    margin-top: ${margin.big};
  }

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

  @media ${Device.mobile} {
    font-size: ${fontSize.small};
  }
`;