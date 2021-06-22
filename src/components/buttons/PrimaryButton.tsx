import React from 'react';
import styled from 'styled-components';
import { Button } from './Button';
import { ButtonColor, getButtonColor } from '../../styles/button-theme';
import { padding } from '../../styles/theme';

const ButtonContainer = styled(Button)`
  padding: ${padding.normal};
  width: 14rem;
  height: 3.5rem;
`;

export interface IPrimaryButton {
  label?: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  color?: ButtonColor;
  fontSize?: string;
  className?: string;
  children?: React.ReactNode;

  onClick?: () => void;
}

export const PrimaryButton: React.FC<IPrimaryButton> = ({
  label,
  icon,
  className,
  disabled,
  color = ButtonColor.Red,
  fontSize,
  onClick,
  children,
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
