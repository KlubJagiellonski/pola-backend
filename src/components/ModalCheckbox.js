import React from 'react'

const ModalCheckbox = ({ dataTestId, value, title }) => {
  return (
    <p>
      <input for={dataTestId} data-testid={dataTestId} type='checkbox' disabled checked={value === 100} />
      <label for={dataTestId}>{title}</label>
    </p>
  )
}

export default ModalCheckbox