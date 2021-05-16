import styled from 'styled-components';
import { color, Device } from '../../styles/theme';

export const Wrapper = styled.div`
  width: 100%;
  padding: 260px 0 70px 0;

  @media only screen and (max-width: 900px) {
    display: flex;
    align-items: center;
    flex-direction: column;
  }

  @media ${Device.mobile} {
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
  color: white;

  @media ${Device.mobile}{
    font-size: 18px;
  }
`;

export const Text = styled.p`
  margin: 10px 0;
  padding: 0;
  font-family: 'Roboto';
  font-size: 16px;
  text-align: left;
  line-height: 1rem;
  color: white;

  @media ${Device.mobile} {
    font-size: 12px;
  }

  a {
    color: #1f1f1f;
  }
`;

export const InputSection = styled.div`
  position: relative;
  border: 1px solid ${color.border};
  padding: 5px 100px 5px 10px;
  width: 320px;
  background-color: white;
  border-radius: 20px;

  @media ${Device.mobile} {
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
  background: white;
  border: 1px solid ${color.border};
  height: 100%;
  font-size: 14px;
  text-align: center;
  padding: 6px 20px;
  margin-left: 15px;
  color: ${color.border};
  display: inline-block;
  font-weight: 700;
  cursor: pointer;
  font-family: 'Roboto';
  border-radius: 20px;

  @media ${Device.mobile} {
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

  @media ${Device.mobile} {
    flex-direction: column;
  }
`;
