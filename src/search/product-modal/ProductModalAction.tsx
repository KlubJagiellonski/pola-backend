import React from 'react';
import styled from 'styled-components';
import { color, padding } from '../../styles/theme';
import { ButtonColor } from '../../styles/button-theme';
import { PrimaryButton } from '../../components/buttons/PrimaryButton';

interface ITheme {
  backgroundColor?: string;
  buttonColor?: ButtonColor;
}

const Container = styled.div<{ theme?: ITheme }>`
  display: flex;
  flex-flow: row nowrap;
  padding: ${padding.normal} ${padding.normal};
  align-items: center;
  border-top: 1px solid ${color.background.primary};
  background-color: ${(props) => props.theme?.backgroundColor || color.background.white};

  .action-btn {
    width: 14rem;
  }
`;

interface IProductModalAction {
  actionName: string;
  theme?: ITheme;

  actionCallback: () => void;
}

export const ProductModalAction: React.FC<IProductModalAction> = ({ actionName, actionCallback, theme, children }) => (
  <Container theme={theme}>
    <div className="content">{children}</div>
    <PrimaryButton color={theme?.buttonColor} label={actionName} className="action-btn" onClick={actionCallback} />
  </Container>
);
