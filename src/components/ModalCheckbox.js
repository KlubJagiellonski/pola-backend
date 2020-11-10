import React from 'react'

import { Wrapper } from './ModalCheckbox.css'

const ModalCheckbox = ({ dataTestId, value, title }) => {
  return (
    <Wrapper>
      <input htmlFor={dataTestId} data-testid={dataTestId} type='checkbox' disabled checked={value === 100} />
      <label htmlFor={dataTestId}>{title}</label>
    </Wrapper>
  )
}

export default ModalCheckbox