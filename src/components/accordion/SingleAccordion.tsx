import React from 'react'
import styled, { keyframes } from 'styled-components';

import {
  AccordionItem,
  AccordionItemHeading,
  AccordionItemButton,
  AccordionItemPanel,
} from 'react-accessible-accordion';
import { ISingleAccordion } from './AccordionList';

const ItemButton = styled(AccordionItemButton)`
  cursor: pointer;
  padding: 10px;
  width: 100%;
  text-align: left;
  border: none;
  font-size: 14px;
  font-weight: bolder;

  ::before{
    display: inline-block;
    content: '';
    height: 7px;
    width: 7px;
    margin-right: 12px;
    border-bottom: 2px solid currentColor;
    border-right: 2px solid currentColor;
    transform: rotate(-135deg);
  }

  &[aria-expanded='true']::before, &[aria-selected='true']::before{
    transform: rotate(45deg);
  }
`
const fadein = keyframes`
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
`;

const ItemPanel = styled(AccordionItemPanel)`
  padding: 10px;
  font-size: 14px;
  animation: ${fadein} 0.35s ease-in;
  padding-left: 30px;
`

const SingleAccordion: React.FC<ISingleAccordion> = ({ question, answer, key }) => {
  return (
    <AccordionItem key={key}>
      <AccordionItemHeading>
        <ItemButton>
          {question}
        </ItemButton>
      </AccordionItemHeading>
      <ItemPanel>
        {answer}
      </ItemPanel>
    </AccordionItem>
  )
}

export default SingleAccordion;