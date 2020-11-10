import styled from "styled-components"

export const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  font-size: 16px;
  overflow: auto;
  max-height: 80vh;
`

export const BigSection = styled.div`
  padding: 0 30px;

  @media only screen and (max-width: 500px) {
    padding: 0;
  }
`

export const SmallSection = styled.div`
  padding: 0 45px;

  @media only screen and (max-width: 500px) {
    padding: 0 10px;
  }
`

export const Section = styled.div`
  margin-top: 10px;
`