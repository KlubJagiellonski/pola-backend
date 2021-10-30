import React from 'react';
import styled, { keyframes } from 'styled-components';
import { lighten } from 'polished';
import { color, fontSize, lineHeight, padding } from '../styles/theme';
import { seconds } from '../domain/generic';

const progressValue = (percetage: number) => keyframes`
    0% {width: 0}
    100% {width: ${`${percetage}%`}}
`;

const Bar = styled.div<{ value: number; animation?: IAniamation }>`
  width: 100%;
  background-color: ${color.background.primary};
  padding: 0;
  text-align: right;
  height: ${lineHeight.big};
  position: relative;

  .value {
    position: absolute;
    background-color: ${lighten(0.1)(color.background.red)};
    height: 100%;
    z-index: 0;

    animation-name: ${(props) => progressValue(props.value)};
    animation-delay: ${({ animation }) => animation?.delay + 's' || 0};
    animation-duration: ${({ animation }) => animation?.duration + 's' || 0};
    animation-iteration-count: ${({ animation }) => animation?.iterations || 1};
    animation-fill-mode: forwards;
    animation-timing-function: ease-out;
    animation-play-state: running;
  }

  .score {
    position: absolute;
    font-size: ${fontSize.small};
    right: ${padding.small};
    width: 100%;
    z-index: 1;
  }
`;

export interface IAniamation {
  duration: seconds;
  delay?: seconds;
  iterations?: number;
}

interface IScoreBar {
  value: number;
  unit?: string;
  animation?: IAniamation;
}

export const ScoreBar: React.FC<IScoreBar> = ({ value, unit, animation }) => {
  const scoreText = unit ? `${value} ${unit}` : value.toString();
  return (
    <Bar value={value} animation={animation}>
      <div className="value" />
      <div className="score">{scoreText}</div>
    </Bar>
  );
};
