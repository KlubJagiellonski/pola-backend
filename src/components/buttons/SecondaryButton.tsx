import React from 'react';
import styled from 'styled-components';
import { Button, IButtonTheme } from './Button';
import { color, Device, fontSize } from '../../styles/theme';

const ButtonContainer = styled(Button)`
  border-radius: 20px;
  border: 2px solid ${color.border.white};
  font-weight: 300;
  text-transform: uppercase;

  @media ${Device.mobile} {
    font-size: ${fontSize.tiny};
  }
`;

export interface ISecondaryButton {
  label?: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  styles: IButtonTheme;
  fontSize?: string;
  className?: string;
  children?: React.ReactNode;

  onClick?: () => void;
}

export const SecondaryButton: React.FC<ISecondaryButton> = ({
  label,
  icon,
  className,
  disabled,
  styles,
  children,
  onClick,
}) => {
  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    !disabled && onClick && onClick();
  };

  return (
    <ButtonContainer theme={styles} className={className} onClick={handleClick} disabled={disabled}>
      {icon}
      {label}
      {children}
    </ButtonContainer>
  );
};
