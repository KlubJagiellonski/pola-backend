import { Link } from 'gatsby';
import React from 'react';
import styled from 'styled-components';
import { ButtonThemes, ButtonFlavor } from './buttons/Button';
import { TitleSection, WrapperSection, Text } from '../styles/GlobalStyle.css';
import { color, fontSize, margin, padding } from '../styles/theme';
import { SecondaryButton } from './buttons/SecondaryButton';

const Wrapper = styled(WrapperSection)`
  margin: 0;
  padding: ${padding.big};
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

const TextInfo = styled(Text)`
  color: ${color.text.light};
  text-align: center;
`;

const ButtonInfoSection = styled.div`
  display: flex;
  justify-content: center;
`;
interface ICard {
  title: string;
  content: string;
  buttonLabel: string;
  url: string;
}

const Card: React.FC<ICard> = ({ title, content, buttonLabel, url }) => {
  return (
    <Wrapper color={color.background.red}>
      <Title>{title}</Title>
      <TextInfo>{content}</TextInfo>
      <ButtonInfoSection>
        <Link to={url}>
          <Button label={buttonLabel} styles={ButtonThemes[ButtonFlavor.RED]} fontSize={fontSize.small} />
        </Link>
      </ButtonInfoSection>
    </Wrapper>
  );
};

export default Card;
