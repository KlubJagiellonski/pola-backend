import React from 'react';
import styled from 'styled-components';
import { IProductEAN } from '../../domain/products';
import { fontSize, padding } from '../../styles/theme';
import { ScoreBar } from '../ScoreBar';
import { Checkbox } from '../../components/checkbox';

const DetailsContainer = styled.div`
  padding: 0 ${padding.normal};
`;

const Field = styled.div`
  margin-bottom: ${padding.normal};
`;

interface IProductDetails {
  product: IProductEAN;
}

export const ProductDetails: React.FC<IProductDetails> = ({ product }) => {
  return (
    <DetailsContainer>
      <h3>{product.name}</h3>
      <Field>
        <span>Punkty w rankingu Poli</span>
        <ScoreBar value={product.data?.score || 0} unit="pkt" />
      </Field>
      <Field>
        <span>udział polskiego kapitału</span>
        <ScoreBar value={product.data?.polishCapital || 0} unit="%" />
      </Field>
      <Field>
        <Checkbox label="produkuje w Polsce" checked={true} disabled={true} />
      </Field>
      <Field>
        <Checkbox label="prowadzi badania i rozwój w Polsce" checked={true} disabled={true} />
      </Field>
      <Field>
        <Checkbox label="zajerestrowana w Polsce" checked={true} disabled={true} />
      </Field>
      <Field>
        <Checkbox label="nie jest częścią zagranicznego koncernu" checked={true} disabled={true} />
      </Field>
      <Field>
        {product.data?.company && <p>{product.data?.company?.name}</p>}
        {product.data?.brand && <p>{product.data?.brand?.name}</p>}
      </Field>
    </DetailsContainer>
  );
};
