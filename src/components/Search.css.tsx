import styled from 'styled-components';
import { theme } from '../styles/theme';

export const Wrapper = styled.div`
  width: 100%;

  @media only screen and (max-width: 900px) {
    padding: 260px 0 70px 0;
    display: flex;
    align-items: center;
    flex-direction: column;
  }

  @media only screen and (max-width: 768px) {
    padding: 100px 0 20px 0;
    display: flex;
    align-items: center;
    flex-direction: column;
  }

  > div {
    @media only screen and (max-width: 400px) {
      width: 90%;
    }
  }
`;

export const Title = styled.p`
  margin: 0;
  padding: 0;
  font-family: 'Roboto';
  font-weight: bold;
  font-size: 24px;
  text-align: left;

  @media only screen and (max-width: 768px) {
    font-size: 18px;
  }
`;

export const Text = styled.p`
  margin: 10px 0;
  padding: 0;
  font-family: 'Roboto';
  font-size: 16px;
  text-align: left;

  @media only screen and (max-width: 768px) {
    font-size: 12px;
  }

  a {
    color: #6c6c6c;
  }
`;

export const InputSection = styled.div`
  position: relative;
  border: 1px solid ${theme.border};
  padding: 5px 100px 5px 5px;
  width: 250px;
  background-color: white;

  @media only screen and (max-width: 768px) {
    width: 100%;
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
    padding: 5px 70px 5px 5px;
  }
`;

export const InputText = styled.input`
  border: none;
  font-size: 14px;
  width: 100%;
`;

export const InputIconSection = styled.div`
  position: absolute;
  top: 0px;
  bottom: 0px;
  display: flex;
  align-items: center;
  right: 10px;
  padding: 3px 0;

  img {
    height: 100%;
    max-height: 20px;
    margin: 3px;
    cursor: pointer;
  }
`;

export const SubmitButton = styled.button`
  background: ${theme.primary};
  border: 1px solid ${theme.border};
  height: 100%;
  font-size: 14px;
  text-align: center;
  padding: 6px 15px;
  margin-left: 15px;
  color: ${theme.border};
  display: inline-block;
  font-weight: 700;
  cursor: pointer;
  font-family: 'Roboto';

  @media only screen and (max-width: 768px) {
    padding: 5px 0;
    margin-left: 0;
    margin-top: 5px;
    width: 100%;
  }
`;

export const FormSearch = styled.div`
  display: flex;
  align-items: center;
  margin-top: 10px;

  @media only screen and (max-width: 768px) {
    flex-direction: column;
  }
`;
