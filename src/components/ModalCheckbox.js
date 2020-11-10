import React from 'react'

const ModalCheckbox = ({ dataTestId, value, title }) => {
  return (
    <p>
      <input htmlFor={dataTestId} data-testid={dataTestId} type='checkbox' disabled checked={value === 100} />
      <label htmlFor={dataTestId}>{title}</label>
    </p>
  )
}

export default ModalCheckbox