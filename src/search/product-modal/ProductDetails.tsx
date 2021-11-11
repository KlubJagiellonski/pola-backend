import React from 'react';
import styled from 'styled-components';
import { Product } from '../../domain/products';
import { padding, fontSize, color } from '../../styles/theme';
import { ScoreBar } from '../../components/ScoreBar';
import { Field, getPropertiesFromManufacturer, PolishPropertyName, ValueCheckboxField } from './PolishValues';
import { AppSettings } from '../../state/app-settings';

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
  const notGlobalProperty = getPropertiesFromManufacturer(manufacturer, PolishPropertyName.NOT_GLOBAL);
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
        {AppSettings.SHOW_POLISH_VALUE_NOTES && <p className="notes">{capitalProperty.notes}</p>}
      </Field>
      <ValueCheckboxField
        condition={workersProperty.value === 100}
        trueLabel="produkuje w Polsce"
        falseLabel="produkuje poza terytorium Polski"
        notes={workersProperty.notes}
      />
      <ValueCheckboxField
        condition={researchProperty.value === 100}
        trueLabel="prowadzi badania i rozwój w Polsce"
        falseLabel="prowadzi badania i rozwój poza terytorium Polski"
        notes={researchProperty.notes}
      />
      <ValueCheckboxField
        condition={registeredProperty.value === 100}
        trueLabel="zajerestrowana w Polsce"
        falseLabel="zajerestrowana poza terytorium Polski"
        notes={registeredProperty.notes}
      />
      <ValueCheckboxField
        condition={notGlobalProperty.value === 100}
        trueLabel="nie jest częścią zagranicznego koncernu"
        falseLabel="jest częścią zagranicznego koncernu"
        notes={notGlobalProperty.notes}
      />
    </DetailsContainer>
  );
};
