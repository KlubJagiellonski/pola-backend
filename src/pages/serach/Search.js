import React, { useState } from 'react'
import SearchModal from './SearchModal';
import axios from 'axios'
import {getCurrentDeviceId} from "../../deviceId";

const Search = () => {
  const [ean, setEan] = useState("")
  const [data, setData] = useState({})
  const [isOpen, setOpen] = useState(false)

  const openModal = () => setOpen({ isOpen: true });
  // const closeModal = () => setOpen({ isOpen: false });

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
    <form onSubmit={handleSubmit}>
      <label>
        Kod EAN:
        <input
            type="text"
            value={ean}
            onChange={e => setEan(e.target.value)}
        />
      </label>

      <button type="submit">Sprawdź</button>
      {
        isOpen &&
        <SearchModal
          data={data}
        />
      }
    </form>
  )
}

export default Search;