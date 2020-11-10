import styled, {keyframes} from "styled-components"

export const Wrapper = styled.div`
  width: 100%;
  position: relative;
`

export const ProgressBarStyled = styled.div`
    height: ${({size}) => size==='big' ? '30px' : '25px'};
    width: 100%;
    background-color: #6c757d;
`

const progress = keyframes`
  from{width: 0;}
`

export const ProgressBarStyledFill = styled.div`
    ${({now})=>
      `width: ${now ? now : 0}%;`
    }
    animation: ${progress} 0.4s linear;
    height: 100%;
    background-color: #d8002f;
`

export const ProgressBarStyledLabel = styled.label`
  margin: 0;
  padding: 0;
  position: absolute;
  right: 10px;
  top: 0;
  bottom: 0;
  color: white;
  display: table-cell;
  vertical-align: middle;
  display: flex;
  justify-content: center;
  align-items: center;
`