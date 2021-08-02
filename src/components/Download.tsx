import React from 'react';
import styled from 'styled-components';

import { color, fontSize, Device, padding, margin } from './../styles/theme';
import { TitleSection } from './../styles/GlobalStyle.css';
import { GooglePlayLink, AppStoreLink } from './links';

const Wrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  min-height: 11.4em;
  padding: ${padding.big} 0;
  background: ${color.background.black};

  @media ${Device.mobile} {
    min-height: 0;
  }
`;

const DownoladTitle = styled(TitleSection)`
  color: ${color.text.light};
  margin: ${margin.normal} 0 ${margin.veryBig} 0;
  font-size: ${fontSize.normal};

  @media ${Device.mobile} {
    ${margin.normal}
  }
`;

const DownloadLinks = styled.div`
  a {
    padding: ${padding.small};

    img {
      @media ${Device.mobile} {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        width: 200px;
      }
    }
  }
`;

const Download = () => {
  return (
    <Wrapper>
      <DownoladTitle>APLIKACJA POLA</DownoladTitle>
      <DownloadLinks>
        <GooglePlayLink />
        <AppStoreLink />
      </DownloadLinks>
    </Wrapper>
  );
};

export default Download;
