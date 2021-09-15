import React from 'react'
import styled from 'styled-components'
import { Accordion } from 'react-accessible-accordion';

import SingleAccordion from './SingleAccordion';

const Wrapper = styled(Accordion)`
  border-radius: 2px;

  [hidden] {
    display: none;
  }
`
export interface ISingleAccordion {
  question: string,
  answer: JSX.Element,
  key: number
}

export interface IAccordionList {
  list: ISingleAccordion[]
}

const AccordionList: React.FC<IAccordionList> = ({ list }) => {
  return (
    <Wrapper allowMultipleExpanded allowZeroExpanded>
      {list.map((item) =>
        <SingleAccordion question={item.question} answer={item.answer} key={item.key} />
      )}
    </Wrapper>
  )
}

export default AccordionList;