import React from 'react'
import { ProgressBarStyled, ProgressBarStyledLabel, Wrapper } from './ModalProgressiveBar.css'

const ModalProgressiveBar = ({now, suffix, size}) => {
  return (
    <Wrapper>
      <ProgressBarStyledLabel>{`${now} ${suffix}`}</ProgressBarStyledLabel>
      <ProgressBarStyled size={size} className='bg-secondary' variant="danger" now={now} />
    </Wrapper>
  )
}

export default ModalProgressiveBar