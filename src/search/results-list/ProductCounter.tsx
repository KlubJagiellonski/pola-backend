import React from 'react';
import styled from 'styled-components';

const CounterText = styled.p<{ fontWeight: string }>`
  font-weight: ${(props) => props.fontWeight};
`;

interface IProductCounter {
  phrase: string;
  amount: number;
}

export const ProductCounter: React.FC<IProductCounter> = ({ phrase, amount }) => {
  if (phrase === undefined || amount === undefined) {
    const text = 'ładownie wyników...';
    return <CounterText fontWeight="normal">{text}</CounterText>;
  } else {
    const postfix = getPolishNumeralPostfix('wynik', amount);
    const text = `${amount} ${postfix} dla "${phrase}"`;
    return <CounterText fontWeight="bold">{text}</CounterText>;
  }
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
