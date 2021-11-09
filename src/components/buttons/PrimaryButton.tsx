import React from 'react';
import styled from 'styled-components';
import { Button, ButtonThemes, IButtonTheme } from './Button';
import { padding } from '../../styles/theme';

const ButtonContainer = styled(Button)`
  padding: ${padding.normal};
  width: 14rem;
`;

export interface IPrimaryButton {
  label?: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  styles?: IButtonTheme;
  className?: string;
  children?: React.ReactNode;

  onClick?: () => void;
}

export const PrimaryButton: React.FC<IPrimaryButton> = ({
  label,
  icon,
  className,
  disabled,
  styles = ButtonThemes.Red,
  onClick,
  children,
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
