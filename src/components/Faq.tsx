import { graphql, useStaticQuery } from 'gatsby';
import React from 'react';
import styled from 'styled-components';
import { TitleSection } from '../styles/GlobalStyle.css';
import { margin } from '../styles/theme';
import AccordionList, { ISingleAccordion } from './accordion/AccordionList';

const Wrapper = styled.div`
  padding-top: 120px;
  margin-top: -120px;
`;

const Section = styled.div`
  margin: ${margin.big} 0;
`;

const Faq = () => {
  const data: IFaqNode = useStaticQuery(graphql`
    {
      faqJson {
        faq {
          id
          question
          answer
        }
      }
    }
  `);

  return (
    <Wrapper id="faq">
      <Section>
        <TitleSection>FAQ</TitleSection>
        <AccordionList list={data.faqJson.faq} />
      </Section>
    </Wrapper>
  );
};

interface IFaqNode {
  faqJson: {
    faq: ISingleAccordion[];
  };
}

export default Faq;
