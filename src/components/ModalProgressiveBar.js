import React from 'react'
import { ProgressBarStyled, ProgressBarStyledLabel, Wrapper, ProgressBarStyledFill } from './ModalProgressiveBar.css'

const ModalProgressiveBar = ({now, suffix, size}) => {
  return (
    <Wrapper>
      <ProgressBarStyledLabel>{`${now} ${suffix}`}</ProgressBarStyledLabel>
      <ProgressBarStyled size={size}>
        <ProgressBarStyledFill now={now}/>
      </ProgressBarStyled>
    </Wrapper>
  )
}

export default ModalProgressiveBar