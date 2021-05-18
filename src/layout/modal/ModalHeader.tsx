import React from 'react';
import styled from 'styled-components';
import { color, Device } from '../../styles/theme';

const Header = styled.div`
  display: flex;
  flex-flow: row nowrap;

  h3 {
    font-weight: bold;
    color: ${color.black};
    flex: 1 1 100%;

    @media ${Device.phone} {
      font-size: 0.8em;
    }
  }
`;

interface IModalHeader {
  title: string;
  onClose: () => void;
}

export const ModalHeader = React.memo((props: IModalHeader) => (
  <Header>
    <h3>{props.title}</h3>
    <button onClick={e => props.onClose()}>X</button>
  </Header>
));
