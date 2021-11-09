import React from 'react';
import styled from 'styled-components';
import { Checkbox } from '../../components/checkbox';
import { IManufacturer } from '../../domain/products';
import { AppSettings } from '../../state/app-settings';
import { padding } from '../../styles/theme';

export const Field = styled.div`
  margin-bottom: ${padding.normal};
`;

export interface IValueCheckbox {
  checked: boolean;
  label: string;
  notes: string;
}

export enum PolishPropertyName {
  WORKERS = 'plWorkers',
  REGISTERED = 'plRegistered',
  CAPITAL = 'plCapital',
  RnD = 'plRnD',
  GLOBAL = 'plNotGlobEnt',
}

export const getPropertiesFromManufacturer = (
  manufacturer: IManufacturer,
  name: PolishPropertyName
): IPolishProperty => {
  const value = manufacturer[name];
  const notes = manufacturer[(name + '_notes') as keyof IManufacturer] as string;

  return { value, notes };
};

export const ValueCheckboxField: React.FC<IValueCheckbox> = ({ checked, label, notes }) => (
  <Field>
    <Checkbox label={label} checked={checked} readonly={true} />
    {AppSettings.SHOW_POLISH_VALUE_NOTES && <p className="notes">{notes}</p>}
  </Field>
);

export interface IPolishProperty {
  value: number;
  notes: string;
}

export interface IPolishPropertyField {
  property: IPolishProperty;
}

export const ProductionField: React.FC<IPolishPropertyField> = ({ property: { value, notes } }) => {
  const checked = value > 50;
  const label = checked ? 'produkuje w Polsce' : 'produkuje poza terytorium Polski';
  return <ValueCheckboxField checked={checked} label={label} notes={notes} />;
};

export const ResearchField: React.FC<IPolishPropertyField> = ({ property: { value, notes } }) => {
  const checked = value > 50;
  const label = checked ? 'prowadzi badania i rozwój w Polsce' : 'prowadzi badania i rozwój poza terytorium Polski';
  return <ValueCheckboxField checked={checked} label={label} notes={notes} />;
};

export const RegisteredField: React.FC<IPolishPropertyField> = ({ property: { value, notes } }) => {
  const checked = value > 50;
  const label = checked ? 'zajerestrowana w Polsce' : 'zajerestrowana poza terytorium Polski';
  return <ValueCheckboxField checked={checked} label={label} notes={notes} />;
};

export const GlobalEntityField: React.FC<IPolishPropertyField> = ({ property: { value, notes } }) => {
  const checked = value === 0;
  const label = checked ? 'nie jest częścią zagranicznego koncernu' : 'jest częścią zagranicznego koncernu';
  return <ValueCheckboxField checked={checked} label={label} notes={notes} />;
};
