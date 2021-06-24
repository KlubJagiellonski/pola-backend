import React from 'react';
import styled from 'styled-components';
import { IProductEAN } from '../../domain/products';
import { Modal } from '../../layout/modal/Modal';
import { color, padding } from '../../styles/theme';
import { ButtonColor } from '../../styles/button-theme';
import { ClickOutside } from '../../utils/click-outside';
import { ProductModalAction } from './ProductModalAction';
import { openNewTab } from '../../utils/browser';
import { urls } from '../../utils/browser/urls';
import { ProductDetails } from './ProductDetails';

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
  product: IProductEAN;
  onClose: () => void;
}

export const ProductModal: React.FC<IProductModal> = ({ product, onClose }) => {
  const reportCallbackMock = () => {
    openNewTab(urls.external.openFoods);
  };
  const downloadCallbackMock = () => {
    openNewTab(urls.external.polaGooglePlay);
  };

  return (
    <ClickOutside clickOutsideHandler={onClose}>
      <Modal title={`EAN: ${product.data?.code}`} onClose={onClose}>
        <ProductDetails product={product} />
        <ProductModalAction actionName={product.report_text} actionCallback={reportCallbackMock}>
          <span>Posiadasz aktualne dane na temat tego produktu?</span>
        </ProductModalAction>
        <ProductModalAction
          theme={{ backgroundColor: color.background.white, buttonColor: ButtonColor.Red }}
          actionName="Pobierz"
          actionCallback={downloadCallbackMock}>
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
