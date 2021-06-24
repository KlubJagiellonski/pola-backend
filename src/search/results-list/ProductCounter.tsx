import React from 'react';
import styled from 'styled-components';
import { padding } from '../../styles/theme';

const CounterText = styled.p`
  padding: ${padding.small} 0;
  font-weight: bold;
`;

interface IProductCounter {
  phrase: string;
  amount: number;
}

export const ProductCounter: React.FC<IProductCounter> = ({ phrase, amount }) => {
  const text = `${amount} ${getPolishNumeralPostfix('wynik', amount)} dla "${phrase}"`;

  return <CounterText>{text}</CounterText>;
};

const getPolishNumeralPostfix = (baseWord: string, amount: number) => {
  const lastDigit = amount % 10;

  let postfix: string = '';
  switch (lastDigit) {
    case 0:
      postfix = 'ów';
      break;
    case 1:
      postfix = amount === 1 ? '' : 'ów';
      break;
    case 2:
    case 3:
    case 4:
      postfix = 10 < amount && amount < 20 ? 'ów' : 'i';
      break;
    default:
      postfix = 'ów';
  }

  return baseWord + postfix;
};
