import React from 'react';
import { Wrapper, DownoladTitle, DownloadLinks} from './Download.css';

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
