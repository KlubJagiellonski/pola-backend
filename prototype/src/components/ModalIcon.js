import React from 'react'

const SearchModalIcon = ({ Icon, ariaLabel, onClick }) => {
  return (
    <Icon
      aria-label={ariaLabel}
      onClick={onClick}
      style={{ color: '#dc3545', fontSize: 30, cursor: 'pointer' }}
    />
  )
}

export default SearchModalIcon;