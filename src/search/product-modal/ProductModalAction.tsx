import React from 'react';
import styled from 'styled-components';
import { color, padding } from '../../styles/theme';
import { IButtonTheme } from '../../components/buttons/Button';
import { PrimaryButton } from '../../components/buttons/PrimaryButton';

interface ITheme {
  backgroundColor?: string;
  buttonTheme?: IButtonTheme;
}

const Container = styled.div<{ theme?: ITheme }>`
  display: flex;
  flex-flow: row nowrap;
  padding: ${padding.normal} ${padding.normal};
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid ${color.background.transparencyGrey};
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
    <PrimaryButton styles={theme?.buttonTheme} label={actionName} className="action-btn" onClick={actionCallback} />
  </Container>
);
