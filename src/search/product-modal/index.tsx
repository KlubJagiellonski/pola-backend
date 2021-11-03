import React from 'react';
import styled from 'styled-components';
import { Product } from '../../domain/products';
import { Modal } from '../../layout/modal/Modal';
import { color, padding } from '../../styles/theme';
import { ButtonFlavor, ButtonThemes } from '../../components/buttons/Button';
import { ClickOutside } from '../../utils/click-outside';
import { ProductModalAction } from './ProductModalAction';
import { navigateTo, openNewTab } from '../../utils/browser';
import { ProductDetails } from './ProductDetails';
import { urls } from '../../domain/website';
import { LinkButton } from '../../components/buttons/LinkButton';

const Actions = styled.div`
  display: flex;
  flex-flow: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
`;

const AppDownload = styled.div`
  h4 {
    margin: 0;
    padding-bottom: ${padding.small};
  }

  .app {
    display: flex;
    flex-flow: row nowrap;
    gap: 0.5rem;

    .image {
      width: 3rem;
      height: 3rem;
      background-color: ${color.button.disabled};
    }
  }
`;

interface IProductModal {
  product: Product;
  onClose: () => void;
}

export const ProductModal: React.FC<IProductModal> = ({ product, onClose }) => {
  const handleReport = () => {
    openNewTab(urls.external.links.openFoods);
  };
  const handleDownloadApp = () => {
    openNewTab(urls.external.links.polaGooglePlay);
  };
  const redirectToFriends = () => {
    onClose();
    navigateTo(urls.pola.friends());
  };
  const handleDonate = () => {
    const donateUrl = new URL(product.donate.url);
    openNewTab(donateUrl);
  };

  return (
    <ClickOutside clickOutsideHandler={onClose}>
      <Modal title={`EAN: ${product.code}`} onClose={onClose}>
        <ProductDetails product={product} />
        <Actions>
          <LinkButton label="Zobacz przyjaciół Poli" styles={ButtonThemes.WhiteRed} onClick={redirectToFriends} />
          {product.donate.show_button && (
            <LinkButton label="Potrzebujemy 1 ZŁ" styles={ButtonThemes.Red} onClick={handleDonate} />
          )}
        </Actions>
        <ProductModalAction actionName={product.report.button_text} actionCallback={handleReport}>
          <span>Posiadasz aktualne dane na temat tego produktu?</span>
        </ProductModalAction>
        <ProductModalAction
          theme={{ backgroundColor: color.background.white, buttonTheme: ButtonThemes[ButtonFlavor.RED] }}
          actionName="Pobierz"
          actionCallback={handleDownloadApp}>
          <AppDownload>
            <h4>Skanuj kody w aplikacji:</h4>
            <div className="app">
              <div className="image" />
              <span>Pola. Zabierz ją na zakupy</span>
            </div>
          </AppDownload>
        </ProductModalAction>
      </Modal>
    </ClickOutside>
  );
};
