import React from 'react';

interface IIconLink {
  height?: number;
}

export const GooglePlayLink: React.FC<IIconLink> = ({ height = 'auto' }) => (
  <a href="https://play.google.com/store/apps/details?id=pl.pola_app">
    <img
      height={height}
      src="https://pola-app.s3.amazonaws.com/images/badge-googleplay.png"
      alt="Pola application on Google Play"
    />
  </a>
);

export const AppStoreLink: React.FC<IIconLink> = ({ height = 'auto' }) => (
  <a href="https://itunes.apple.com/us/app/pola.-zabierz-ja-na-zakupy/id1038401148?ls=1&amp;mt=8">
    <img
      height={height}
      src="https://pola-app.s3.amazonaws.com/images/badge-appstore.png"
      alt="Pola application on App Store"
    />
  </a>
);
