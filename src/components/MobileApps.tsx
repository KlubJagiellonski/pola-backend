import React from 'react';
import styled from 'styled-components';
import { urls } from '../domain/website';
import { AppSettings } from '../state/app-settings';
import { Device, padding } from './../styles/theme';

const DownloadLinks = styled.div`
  display: flex;
  align-items: center;
  a {
    padding: ${padding.small};

    img {
      @media ${Device.mobile} {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        width: 8em;
      }
    }
  }
`;

interface IMobileApps {
  size?: number;
}

export const MobileApps: React.FC<IMobileApps> = ({ size = 64 }) => {
  return (
    <DownloadLinks>
      {AppSettings.mobile.SHOW_APPLE_STORE_LINK && <AppStoreLink height={size} />}
      {AppSettings.mobile.SHOW_GOOGLE_PLAY_LINK && <GooglePlayLink height={size} />}
      {AppSettings.mobile.SHOW_HUAWEI_GALLERY_LINK && <HuaweiAppGalleryLink height={size * 1.4} />}
    </DownloadLinks>
  );
};

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
