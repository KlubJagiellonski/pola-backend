import React from 'react';
import styled from 'styled-components';
import { Modal } from '../../layout/modal/Modal';
import { padding } from '../../styles/theme';
import { ClickOutside } from '../../utils/click-outside';

const Info = styled.div`
  display: flex;
  flex-flow: column;
  align-items: center;
  gap: 1rem;
  padding: ${padding.small} ${padding.normal};
`;

interface ISearchInfoModal {
  onClose: () => void;
}

export const SearchInfoModal: React.FC<ISearchInfoModal> = ({ onClose }) => {
  return (
    <ClickOutside clickOutsideHandler={onClose}>
      <Modal title="Sprawdź informacje o produkcie" styles={{ height: '20rem' }} onClose={onClose}>
        <Info>
          <p>
            Jeśli chcesz znaleźć produkty polskich firm, możesz wkleić lub wpisać w polu tekstowym kod EAN dowolnego
            produktu. Kod znajdziesz na opakowaniu lub w opisie produktu na stronie sklepu internetowego. Możesz także
            wpisać nazwę producenta lub nazwę produktu.
          </p>
          <span>Jeśli potrzebujesz więcej informacji lub chcesz zgłosić błąd, prosimy o kontakt:</span>
          <a href="mailto:pola@klubjagiellonski.pl">pola@klubjagiellonski.pl</a>
        </Info>
      </Modal>
    </ClickOutside>
  );
};
