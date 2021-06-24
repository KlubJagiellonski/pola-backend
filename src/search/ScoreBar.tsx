import React from 'react';
import styled from 'styled-components';
import { lighten } from 'polished';
import { color, lineHeight, padding } from '../styles/theme';

const Bar = styled.div<{ value: number }>`
  width: 100%;
  background-color: ${color.background.primary};
  padding: 0;
  text-align: right;
  height: ${lineHeight.big};
  position: relative;

  .value {
    position: absolute;
    background-color: ${lighten(0.2)(color.background.red)};
    height: 100%;
    width: ${(props) => `${props.value}%`};
    z-index: 0;
  }

  .score {
    width: 100%;
    position: absolute;
    padding-right: ${padding.normal};
    z-index: 1;
  }
`;

interface IScoreBar {
  value: number;
  unit?: string;
}

export const ScoreBar: React.FC<IScoreBar> = ({ value, unit }) => {
  const scoreText = unit ? `${value} ${unit}` : value.toString();
  return (
    <Bar value={value}>
      <div className="value" />
      <div className="score">{scoreText}</div>
    </Bar>
  );
};
