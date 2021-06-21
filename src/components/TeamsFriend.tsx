import React from 'react';
import styled from 'styled-components';

import { WrapperTeams, Title, TextSection, ButtonTeams } from './Teams.css';
import { Text } from '../styles/GlobalStyle.css';
import { color } from '../styles/theme';
import { ButtonColor } from '../styles/button-theme';
import Icon from './../assets/ikona-zespół.png';

const Wrapper = styled(WrapperTeams)`
  grid-area: teams-friend;
`;

const TeamsFriend = () => {
  return (
    <Wrapper color={color.background.white}>
      <TextSection>
        <img src={Icon} />
        <Title>Dołącz do Przyjaciół Poli i odnieś sukces!</Title>
        <Text>Jedno zdanie, że sekcja jest kierowana do firm</Text>
        <ButtonTeams label="POZNAJ SZCZEGÓŁY" color={ButtonColor.Red} />
      </TextSection>
    </Wrapper>
  );
};

export default TeamsFriend;
