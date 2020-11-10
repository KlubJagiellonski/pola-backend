import styled from "styled-components"

export const Wrapper = styled.div`
    width: 50%;
    margin: 0 auto;
`

export const Text = styled.p`
    font-size: 24px;
    text-align: center;

    a{
        color: blue;
        text-decoration: none;
    }
`

export const SearchButton = styled.button`
    color: #d8002f;
    float: left;
    text-align: center;
    display: flex;
    justify-content: center;
    position: absolute;
    right: 20px;
    cursor: pointer;
    border: none;
    background: none;
    font-size: 32px;
`
export const SearchInput = styled.input`
    width: 100%;
    padding-left: 15px;
    border: none;
    color: #495057;
    padding-right: 70px;
    font-size: 32px;
`

export const SearchFormControl = styled.form`
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    width: 100%;
    border: solid 4px #d8002f;
    margin: 0 auto;
    margin-bottom: 1rem;
    position: relative;
    padding: 5px 0;
`