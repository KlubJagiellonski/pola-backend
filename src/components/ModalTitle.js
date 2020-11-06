import React from 'react'
import {  WrapperTitle, Title } from './ModalTitle.css'
import ModalIcon from './ModalIcon'
import { FaTimesCircle } from 'react-icons/fa'
// import { RiFileCopyLine } from 'react-icons/ri'

const SearchModalTitle = ({ title, close }) => {
  return (
    <WrapperTitle>
      <ModalIcon Icon={FaTimesCircle} onClick={close} />
      <Title>
        {title}
      </Title>
    </WrapperTitle>
  )
}

export default SearchModalTitle;