import React from 'react';
import styled from 'styled-components';
import { Product } from '../../domain/products';
import { padding, fontSize, color } from '../../styles/theme';
import { ScoreBar } from '../../components/ScoreBar';
import {
  Field,
  ProductionField,
  ResearchField,
  RegisteredField,
  GlobalEntityField,
  getPropertiesFromManufacturer,
  PolishPropertyName,
} from './PolishValues';

const DetailsContainer = styled.div`
  padding: ${padding.normal};
  border-top: 1px solid ${color.background.transparencyGrey};

  header {
    display: flex;
    flex-flow: column;
    align-items: start;
    margin-bottom: 1em;
  }

  .property,
  .notes {
    margin-top: 0.5em;
  }

  .notes {
    font-size: ${fontSize.small};
  }

  .property {
    margin-bottom: 0.25em;
  }
`;

interface IProductDetails {
  product: Product;
}

export const ProductDetails: React.FC<IProductDetails> = ({ product }) => {
  const manufacturer = product.manufacturer;
  const workersProperty = getPropertiesFromManufacturer(manufacturer, PolishPropertyName.WORKERS);
  const researchProperty = getPropertiesFromManufacturer(manufacturer, PolishPropertyName.RnD);
  const registeredProperty = getPropertiesFromManufacturer(manufacturer, PolishPropertyName.REGISTERED);
  const globalProperty = getPropertiesFromManufacturer(manufacturer, PolishPropertyName.GLOBAL);
  const capitalProperty = getPropertiesFromManufacturer(manufacturer, PolishPropertyName.CAPITAL);

  return (
    <DetailsContainer>
      <header>
        <h3>{product.name}</h3>
      </header>
      <Field>
        <p className="property">Producent: {product.manufacturer.name}</p>
      </Field>
      <Field>
        <p className="property">Punkty w rankingu Poli:</p>
        <ScoreBar value={product.manufacturer.plScore || 0} unit="pkt" animation={{ duration: 1, delay: 0.2 }} />
      </Field>
      <Field>
        <p className="property">udział polskiego kapitału:</p>
        <ScoreBar value={capitalProperty.value || 0} unit="%" animation={{ duration: 1, delay: 0.2 }} />
        <p className="notes">{capitalProperty.notes}</p>
      </Field>
      <ProductionField property={workersProperty} />
      <ResearchField property={researchProperty} />
      <RegisteredField property={registeredProperty} />
      <GlobalEntityField property={globalProperty} />
    </DetailsContainer>
  );
};
