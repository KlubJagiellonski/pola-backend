import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom';
import SearchModal from './SearchModal';
import axios from 'axios'
import { getCurrentDeviceId } from "../../deviceId";
import { Background, Content, Wrapper } from "./Modal.css";
import { Redirect } from "react-router-dom";

const ModalPage = ({ match, open }) => {
  const [data, setData] = useState('');
  const { ean } = useParams();

  const [isRedirect, setRedirect] = useState(false)

  const closeModal = () => {
    setRedirect(true)
  }

  useEffect((ean) => {
    async function api() {
      if (ean && ean.length > 0) {
        try {
          const resp = await axios.get('https://www.pola-app.pl/a/v3/get_by_code',
            {
              params: {
                code: ean,
                device_id: getCurrentDeviceId()
              }
            })
          setData(resp.data)
        } catch (err) {
          console.log(err)
        }
      }
    }
    api()
  }, [ean]);

  return (
    <>
      { isRedirect ?
        <Redirect to='/' /> :
        <>
          <Background>
            <Wrapper onClick={closeModal} />
            <Content open={open}>
              <SearchModal
                data={data}
                close={closeModal}
              />
            </Content>
          </Background>

        </>
      }
    </>
  )
}

export default ModalPage;