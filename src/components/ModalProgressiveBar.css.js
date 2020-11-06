import styled from "styled-components"
import { ProgressBar } from "react-bootstrap"

export const Wrapper = styled.div`
  width: 100%;
  position: relative;
`

export const ProgressBarStyled = styled(ProgressBar)`
    height: ${({size}) => size==='big' ? '30px' : '25px'};
    border-radius: 0;
`

export const ProgressBarStyledLabel = styled.label`
  margin: 0;
  padding: 0;
  position: absolute;
  right: 10px;
  top: 0;
  bottom: 0;
  color: white;
`