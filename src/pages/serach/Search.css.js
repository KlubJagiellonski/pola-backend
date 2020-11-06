import styled from "styled-components"
import { FormControl, Button } from "react-bootstrap"

export const SearchButton = styled(Button)`
    background-color: transparent;
    border: solid 4px #d8002f;
    border-left: none;
    color: #d8002f;
    font-size: 28px;
    padding: 0 20px;
    :hover{
        background-color: transparent;
        border: solid 4px #d8002f;
        border-left: none;
        color: #d8002f;
        box-shadow: none;
        font-size: 35px;
    }
   :focus,:active {
        outline: none !important;
        box-shadow: none !important;
        background-color: transparent !important;
        border: solid 4px #d8002f !important;
        border-left: none !important;
        color: #d8002f !important;
     }
`
export const SearchFormControl = styled(FormControl)`
    border: solid 4px #d8002f;
    border-right: none;
    font-size: 32px;
    padding-left: 15px;
    :focus{
        box-shadow: none;
        border: solid 4px #d8002f;
        border-right: none;
    }
`