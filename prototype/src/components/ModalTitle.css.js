import styled, {keyframes} from "styled-components"

export const WrapperTitle = styled.div`
  display: flex;
  flex-direction: row;
  width: 100%;
  margin-bottom: 10px;
`

export const Title = styled.p`
  width: 100%;
  fontSize: 20px;
  padding: 0 10px; 
  margin: 0;
`

const toolTip = keyframes`
  0%{
    opacity: 0;
  }
  30%{
    opacity: 1;
  }
  70%{
    opacity: 1;
  }
  100%{
    opacity: 0;
  }
`

export const ToolTip = styled.div`
    opacity: 1;
    position: absolute;
    background-color: #253037;
    color: white;
    transform: translate(50%, 100%);
    padding: 5px 20px;
    right: 15px;
    z-index: 999;
    white-space: nowrap;
    border-radius: 10px;
    animation: ${toolTip} 1s linear;
`