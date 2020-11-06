import React from 'react'

const SearchModalIcon = ({ Icon, onClick }) => {
  return (
    <Icon
      onClick={onClick}
      style={{ color: '#dc3545', fontSize: 30, cursor: 'pointer' }}
    />
  )
}

export default SearchModalIcon;