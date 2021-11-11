import React from 'react';
import styled from 'styled-components';
import { urls } from '../domain/website';
import { AppSettings } from '../state/app-settings';
import { Device, padding, px } from './../styles/theme';

interface IIconLink {
  size?: number;
}

const Image = styled.img<IIconLink>`
  height: ${({ size }) => (size ? px(size) : 'auto')};
`;

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
      {AppSettings.mobile.SHOW_APPLE_STORE_LINK && <AppStoreLink size={size} />}
      {AppSettings.mobile.SHOW_GOOGLE_PLAY_LINK && <GooglePlayLink size={size} />}
      {AppSettings.mobile.SHOW_HUAWEI_GALLERY_LINK && <HuaweiAppGalleryLink size={size * 1.4} />}
    </DownloadLinks>
  );
};

export const GooglePlayLink: React.FC<IIconLink> = ({ size = 'auto' }) => (
  <a href={urls.external.links.polaGooglePlay.href}>
    <Image
      height={size}
      src="https://pola-app.s3.amazonaws.com/images/badge-googleplay.png"
      alt="Pola application on Google Play"
    />
  </a>
);

export const AppStoreLink: React.FC<IIconLink> = ({ size = 'auto' }) => (
  <a href={urls.external.links.polaAppStore.href}>
    <Image
      height={size}
      src="https://pola-app.s3.amazonaws.com/images/badge-appstore.png"
      alt="Pola application on App Store"
    />
  </a>
);

export const HuaweiAppGalleryLink: React.FC<IIconLink> = ({ size = 'auto' }) => (
  <a href={urls.external.links.polaHuaweiAppGallery.href}>
    <Image
      style={{ margin: '-10px' }} // for this specific PNG as there is transparent space around logotype
      height={size}
      src="https://www.newseria.pl/files/_uploaded/glownekonf_37779598.png"
      alt="Pola application on Huawei Store"
    />
  </a>
);
