import styled from "styled-components"
import { Link } from "react-router-dom";

export const SearchButton = styled(Link)`
    color: #d8002f;
    float: left;
    text-align: center;
    display: flex;
    justify-content: center;
    position: absolute;
    right: 20px;
    cursor: pointer;
`
export const SearchInput = styled.input`
    width: 100%;
    padding-left: 15px;
    border: none;
    color: #495057;
    padding-right: 70px;
`

export const SearchFormControl = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    padding: 2.5px 0;
    width: 50%;
    border: solid 4px #d8002f;
    font-size: 32px;
    margin: 0 auto;
    margin-bottom: 1rem;
    position: relative;
`