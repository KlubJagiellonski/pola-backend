import React from 'react';
import { urls } from '../../domain/website';

interface IIconLink {
  height?: number;
}

export const GooglePlayLink: React.FC<IIconLink> = ({ height = 'auto' }) => (
  <a href={urls.external.links.polaGooglePlay.href}>
    <img
      height={height}
      src="https://pola-app.s3.amazonaws.com/images/badge-googleplay.png"
      alt="Pola application on Google Play"
    />
  </a>
);

export const AppStoreLink: React.FC<IIconLink> = ({ height = 'auto' }) => (
  <a href={urls.external.links.polaAppStore.href}>
    <img
      height={height}
      src="https://pola-app.s3.amazonaws.com/images/badge-appstore.png"
      alt="Pola application on App Store"
    />
  </a>
);

export const HuaweiAppGalleryLink: React.FC<IIconLink> = ({ height = 'auto' }) => (
  <a href={urls.external.links.polaHuaweiAppGallery.href}>
    <img
      style={{ margin: '-10px' }} // for this specific PNG as there is transparent space around logotype
      height={height}
      src="https://www.newseria.pl/files/_uploaded/glownekonf_37779598.png"
      alt="Pola application on Huawei Store"
    />
  </a>
);
