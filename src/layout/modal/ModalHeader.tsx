import React from 'react';
import styled from 'styled-components';
import { IconButton } from '../../components/buttons/IconButton';
import { color, Device, fontSize, padding } from '../../styles/theme';

const Header = styled.div`
  display: flex;
  flex-flow: row nowrap;
  padding: ${padding.small} ${padding.normal};
  align-items: baseline;

  h3 {
    font-weight: bold;
    color: ${color.text.dark};
    flex: 1 1 100%;
    margin: 0;

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
    <IconButton icon={<span>X</span>} onClick={props.onClose} />
  </Header>
));
