import React from 'react';
import styled from 'styled-components';
import { Button, ButtonThemes, IButtonTheme } from './Button';
import { padding } from '../../styles/theme';

const ButtonContainer = styled(Button)`
  padding: ${padding.small};
  min-width: 16rem;
  border-radius: 0;
`;

export interface ILinkButton {
  label?: string;
  icon?: React.ReactNode;
  disabled?: boolean;
  styles: IButtonTheme;
  className?: string;
  children?: React.ReactNode;

  onClick?: () => void;
}

export const LinkButton: React.FC<ILinkButton> = ({
  label,
  icon,
  className,
  disabled,
  styles = ButtonThemes.WhiteRed,
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
