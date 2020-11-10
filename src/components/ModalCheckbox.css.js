import styled from "styled-components"

export const Wrapper = styled.p`
  [type="checkbox"]:not(:checked),
  [type="checkbox"]:checked {
    position: absolute;
    left: -9999px;
  }
  [type="checkbox"]:not(:checked) + label,
  [type="checkbox"]:checked + label {
    position: relative;
    padding-left: 1.95em;
    cursor: pointer;
  }

  [type="checkbox"]:not(:checked) + label:before,
  [type="checkbox"]:checked + label:before {
    content: "";
    position: absolute;
    left: 0; 
    top: 0;
    width: 1.5em; 
    height: 1.5em;
    border: 2px solid #ccc;
    background: #fff;
    border-radius: 10%;
  }

  [type="checkbox"]:not(:checked) + label:after,
  [type="checkbox"]:checked + label:after {
    content: "✓";
    position: absolute;
    top: .15em; 
    left: .22em;
    font-size: 1.3em;
    line-height: 0.8;
    color: #09ad7e;
    transition: all .2s;
    font-family: 'Lucida Sans Unicode', 'Arial Unicode MS', Arial;
  }

  [type="checkbox"]:not(:checked) + label:after {
    opacity: 0;
    transform: scale(0);
  }
  [type="checkbox"]:checked + label:after {
    opacity: 1;
    transform: scale(1);
  }
  
  [type="checkbox"]:disabled:not(:checked) + label:before,
  [type="checkbox"]:disabled:checked + label:before {
    box-shadow: none;
    border-color: #6c757d;
    background-color: #6c757d;
  }
  [type="checkbox"]:disabled:checked + label:after {
    color: white;
  }
  [type="checkbox"]:disabled + label {
    color: black;
  }
`