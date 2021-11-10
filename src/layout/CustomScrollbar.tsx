import React from 'react';
import styled from 'styled-components';
import { color, padding } from '../styles/theme';

export const CustomScrollbarDiv = styled.div`
  ::-webkit-scrollbar {
    width: ${padding.small};
  }

  ::-webkit-scrollbar-track {
    background: ${color.background.white};
  }

  ::-webkit-scrollbar-thumb {
    background: ${color.border.grey};
  }

  overflow-x: hidden;
  overflow-y: auto;
`;
