import React from 'react';
import styled from 'styled-components';

import {color, fontSize, Device, padding, margin} from './../styles/theme'
import {TitleSection} from './../styles/GlobalStyle.css'

const Wrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  min-height: 11.4em;
  padding: ${padding.big} 0;

  @media ${Device.mobile}{
    min-height: 0;
  }
`;

const DownoladTitle = styled(TitleSection)`
  color: ${color.text.light};
  margin: ${margin.normal} 0 ${margin.veryBig} 0;
  font-size: ${fontSize.normal};

  @media ${Device.mobile}{
    ${margin.normal}
  }
`

const DownloadLinks = styled.div`
  a{
    padding: ${padding.small};

    img{

      @media ${Device.mobile}{
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        width: 200px;
      }
    }
  }
`


const Download = () => {
  return (
    <Wrapper>
      <DownoladTitle>APLIKACJA POLA</DownoladTitle>
      <DownloadLinks>
        <a href="https://play.google.com/store/apps/details?id=pl.pola_app">
          <img src="https://pola-app.s3.amazonaws.com/images/badge-googleplay.png" alt=""/>
        </a>
        <a href="https://itunes.apple.com/us/app/pola.-zabierz-ja-na-zakupy/id1038401148?ls=1&amp;mt=8">
          <img src="https://pola-app.s3.amazonaws.com/images/badge-appstore.png" alt=""/>
        </a>
      </DownloadLinks>
    </Wrapper>
  );
};

export default Download;
