import React from 'react';
import styled from 'styled-components';
import { Button } from './Button';
import { ButtonColor, getButtonColor } from '../../styles/button-theme';
import { color } from '../../styles/theme';

const ButtonContainer = styled(Button)`
  border-radius: 20px;
  border: 2px solid ${color.border.white};
  font-weight: 300;
  text-transform: uppercase; 
`;

export interface ITagButton {
  label?: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  color?: ButtonColor;
  fontSize?: string;
  className?: string;
  children?: React.ReactNode;

  onClick?: () => void;
}

export const TagButton: React.FC<ITagButton> = ({
  label,
  icon,
  className,
  disabled,
  color,
  fontSize,
  children,
  onClick,
}) => {
  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    !disabled && onClick && onClick();
  };

  const themeColor = getButtonColor(color);

  const theme = {
    color: themeColor,
    fontSize,
  };

  return (
    <ButtonContainer theme={theme} className={className} onClick={handleClick} disabled={disabled}>
      {icon}
      {label}
      {children}
    </ButtonContainer>
  );
};
