import React from 'react';
import { IProductEAN } from '../../domain/products';
import { Modal } from '../../layout/modal/Modal';

interface IProductModal {
  product: IProductEAN;
  onClose: () => void;
}

export const ProductModal: React.FC<IProductModal> = ({ product, onClose }) => (
  <Modal title={`EAN: ${product.code}`} onClose={onClose}>
    <h3>{product.name}</h3>
  </Modal>
);
