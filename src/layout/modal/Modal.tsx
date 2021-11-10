import React from 'react';
import styled from 'styled-components';
import { color, Device, padding } from '../../styles/theme';
import { CustomScrollbarDiv } from '../CustomScrollbar';
import { ModalHeader } from './ModalHeader';

const ModalLayout = styled.div`
  position: fixed;
  display: flex;
  width: 100%;
  height: 100vh;
  z-index: 100;
  justify-content: center;
  align-items: center;
`;

const ModalContainer = styled.div<{ height?: string }>`
  background-color: ${color.background.white};
  position: absolute;
  overflow: hidden;
  display: flex;
  flex-flow: column;
  min-height: 12rem;
  height: ${(props) => props.height || '85vh'};
  z-index: 1;
  max-width: 800px;
  box-sizing: border-box;

  header {
    display: flex;
    flex-flow: row nowrap;
    align-items: center;

    .title-container {
      flex: 1 1 100%;
    }
  }

  @media ${Device.phone} {
    width: calc(100% - 2 * ${padding.small});
  }
  @media ${Device.desktop} {
    width: calc(100% - 2 * ${padding.big});
  }
`;

const ModalContent = styled(CustomScrollbarDiv)`
  flex: 1 1 100%;
`;

const ModalOverlay = styled.div`
  background-color: ${color.background.black};
  width: 100%;
  height: 100vh;
  opacity: 0.5;
  z-index: 0;
`;

interface IModal {
  title: string;
  styles?: {
    height?: string;
  };
  onClose: () => void;
}

export const Modal: React.FC<IModal> = ({ title, onClose, children, styles }) => (
  <ModalLayout>
    <ModalOverlay />
    <ModalContainer height={styles?.height}>
      <ModalHeader title={title} onClose={onClose} />
      <ModalContent>{children}</ModalContent>
    </ModalContainer>
  </ModalLayout>
);
