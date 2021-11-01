import { Link } from 'gatsby';
import React from 'react';
import styled from 'styled-components';
import { ButtonThemes, ButtonFlavor } from './buttons/Button';
import { TitleSection, WrapperSection } from '../styles/GlobalStyle.css';
import { color, fontSize, margin, padding } from '../styles/theme';
import { SecondaryButton } from './buttons/SecondaryButton';

const Wrapper = styled(WrapperSection)`
  margin: 0;
  padding: ${padding.big};
  text-align: center;

  * {
    color: ${color.text.light} !important;
  }
`;

const Button = styled(SecondaryButton)`
  text-transform: capitalize;
  font-weight: bold;
  min-width: 300px;
`;

const Title = styled(TitleSection)`
  text-align: center;
  color: ${color.text.light};
  margin-bottom: ${margin.big};
`;

const ButtonInfoSection = styled.div`
  display: flex;
  justify-content: center;
`;
interface ICard {
  title: string;
  chidlren?: JSX.Element;
  buttonLabel?: string;
  url: string;
}

const Card: React.FC<ICard> = ({ title, children, buttonLabel, url }) => {
  return (
    <Wrapper color={color.background.red}>
      <Title>{title}</Title>
      {children}
      {buttonLabel && (
        <ButtonInfoSection>
          <Link to={url}>
            <Button label={buttonLabel} styles={ButtonThemes[ButtonFlavor.RED]} fontSize={fontSize.small} />
          </Link>
        </ButtonInfoSection>
      )}
    </Wrapper>
  );
};

export default Card;
