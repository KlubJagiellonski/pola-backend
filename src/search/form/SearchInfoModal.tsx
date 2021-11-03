import React from 'react';
import styled from 'styled-components';
import { urls } from '../../domain/website';
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
            produktu. Kod znajdziesz na opakowaniu, w opisie produktu na stronie sklepu internetowego lub w&nbsp;
            <a target="blank" href={urls.external.links.openFoods.href}>
              bazie Open Foods
            </a>
          </p>
          <span>
            Możesz także wpisać nazwę producenta lub nazwę produktu. Jeśli potrzebujesz więcej informacji lub chcesz
            zgłosić błąd, prosimy o kontakt:
          </span>
          <a href="mailto:pola@klubjagiellonski.pl">pola@klubjagiellonski.pl</a>
        </Info>
      </Modal>
    </ClickOutside>
  );
};
