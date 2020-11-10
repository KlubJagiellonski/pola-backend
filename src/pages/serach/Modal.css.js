import styled, { keyframes } from "styled-components"

export const filling = keyframes`
  from {
    background-color: rgba(0, 0, 0, 0);
  }

  to {
    background-color: rgba(0, 0, 0, 0.5);
  }
`

export const Background = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  animation: ${filling} 0.3s linear;
  background-color: rgba(0, 0, 0, 0.5);
`

export const Wrapper = styled.div`
  position: absolute;
  width: 100vw;
  height: 100vh;
  z-index: -1;
`

export const translate = keyframes`
  from {
    transform: translate(0, -40%);
  }

  to {
    transform: translate(0, 0);
  }
`

export const Content = styled.div`
  width: 50%;
  padding: 16px;
  margin: 30px auto;
  background-color: white;
  border-radius: 5px;
  box-shadow: 10px 10px 15px rgba(0, 0, 0, 0.2);
  animation: ${translate} 0.3s linear;
`
