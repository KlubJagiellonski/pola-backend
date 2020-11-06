import React, { useState } from 'react'
import SearchModal from './SearchModal';
import axios from 'axios'
import {getCurrentDeviceId} from "../../deviceId";
import { InputGroup, Modal } from "react-bootstrap"
import { SearchButton, SearchFormControl } from "./Search.css"
import { ImSearch } from 'react-icons/im'

const Search = () => {
  const [ean, setEan] = useState("")
  const [data, setData] = useState({})
  const [isOpen, setOpen] = useState(false)

  const openModal = () => setOpen(true);
  const closeModal = () => setOpen(false);

  const handleSubmit = async(e) => {
    e.preventDefault();
    if (ean.length > 0) {
        try {
           const resp = await axios.get('/get_by_code',
            {
              params: {
                code: ean,
                device_id: getCurrentDeviceId()
              }
            })

            openModal();
            setData(resp.data)
        } catch(err) {
            console.log(err)
        }
    }
  }

  return (
    <div style={{ width: '100%' }}>
      <form style={{ width: '50%', margin: '0 auto' }} onSubmit={handleSubmit}>
        <InputGroup className="mb-3 border-0 w-100" >
          <SearchFormControl
            type='text'
            value={ean}
            onChange={e => setEan(e.target.value)}
            placeholder="Wpisz tutaj kod kreskowy"
          />
          <InputGroup.Append>
            <SearchButton type='submit' variant="outline-secondary">
              <ImSearch />
            </SearchButton>
          </InputGroup.Append>
        </InputGroup>
      </form>
      <Modal
        size="lg"
        show={isOpen}
        onHide={closeModal}
        aria-labelledby="example-modal-sizes-title-lg"
      >
        <Modal.Body>
          <SearchModal
            data={data}
            close={closeModal}
          />
        </Modal.Body>
      </Modal>
    </div >
  )
}

export default Search;