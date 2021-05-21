import React from 'react';
import styled from 'styled-components';
import { IProductEAN } from '../../domain/products';
import { Modal } from '../../layout/modal/Modal';
import { color, padding } from '../../styles/theme';
import { ButtonColor } from '../buttons/Button';
import { ClickOutside } from '../ClickOutside';
import { ProductModalAction } from './ProductModalAction';

const ProductDetails = styled.div`
  padding: ${padding.small} ${padding.normal};
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
      background-color: ${color.border};
    }
  }
`;

interface IProductModal {
  product: IProductEAN;
  onClose: () => void;
}

export const ProductModal: React.FC<IProductModal> = ({ product, onClose }) => {
  const reportCallbackMock = () => true;
  const friendsCallbackMock = () => true;
  const downloadCallbackMock = () => true;

  return (
    <ClickOutside clickOutsideHandler={onClose}>
      <Modal title={`EAN: ${product.code}`} onClose={onClose}>
        <ProductDetails>
          <h3>{product.name}</h3>
          <ul>
            <li>{product.name}</li>
            <li>{product.code}</li>
          </ul>
        </ProductDetails>
        <ProductModalAction actionName={product.report_text} actionCallback={reportCallbackMock}>
          <span>Posiadasz aktualne dane na temat tego produktu?</span>
        </ProductModalAction>
        <ProductModalAction actionName="Button" actionCallback={friendsCallbackMock}>
          <span>MIEJSCE NA PRZYJACIÓŁ?</span>
        </ProductModalAction>
        <ProductModalAction
          actionName="Pobierz"
          theme={{ backgroundColor: color.primary, buttonColor: ButtonColor.Red }}
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
