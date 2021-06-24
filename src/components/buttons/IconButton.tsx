import React from 'react';
import styled from 'styled-components';
import { color, fontSize, padding } from '../../styles/theme';

const Button = styled.button`
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  cursor: pointer;
  color: ${color.text.primary};
  background-color: ${color.button.white};
  border: none;
  padding: ${padding.normal};
  font-size: ${fontSize.big};
  white-space: nowrap;
  font-weight: bold;
  width: 1.4rem;
  height: 1.4rem;

  &:focus {
    outline: none;
  }

  &.disabled {
    cursor: default;
    background-color: ${color.button.disabled};
    font-weight: 400;
  }
`;

export interface IIconButton {
  icon: React.ReactNode;
  disabled?: boolean;
  className?: string;

  onClick?: () => void;
}

export const IconButton: React.FC<IIconButton> = ({ icon, className, disabled, onClick }) => {
  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    !disabled && onClick && onClick();
  };

  return (
    <Button className={className} onClick={handleClick}>
      {icon}
    </Button>
  );
};
