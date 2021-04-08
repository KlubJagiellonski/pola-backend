import React, { useState, useEffect } from 'react'
import SearchModal from './SearchModal';
import axios from 'axios'
import { getCurrentDeviceId } from "../../deviceId";
import { Background, Content, Wrapper } from "./Modal.css";
import { Redirect, useParams } from "react-router-dom";

const BASE_URL = process.env.NODE_ENV !== 'production' ? "" : "https://www.pola-app.pl"
const GET_BY_CODE_ENDPOINT = `${BASE_URL}/a/v3/get_by_code`

const ModalPage = () => {
  const [data, setData] = useState('');
  const { ean } = useParams();

  const [isRedirect, setRedirect] = useState(false)

  const closeModal = () => {
    setRedirect(true)
  }

  useEffect(() => {
    let isCancelled = false;
    async function api() {
      try {
        const resp = await axios.get(GET_BY_CODE_ENDPOINT,
          {
            params: {
              code: ean,
              device_id: getCurrentDeviceId()
            }
          })
        if (!isCancelled) {
          setData(resp.data)
        }
      } catch (err) {
        console.log(err)
      }
    }
    api()
    return () => {
      isCancelled = true;
    };
  }, [ean]);

  return (
    <>
      {isRedirect ?
        <Redirect to='/' /> :
        <>
          <Background>
            <Wrapper onClick={closeModal} />
            <Content>
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