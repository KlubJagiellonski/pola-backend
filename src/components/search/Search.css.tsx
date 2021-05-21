import styled from 'styled-components';
import { color, Device, fontSize, margin, padding } from '../../styles/theme';
import {SecondaryButton} from './../buttons/SecondaryButton';

export const Wrapper = styled.div`
  width: 100%;
  padding: 260px 0 70px 0;
  position: relative;

  @media ${Device.mobile} {
    padding: 100px 0 20px 0;
    display: flex;
    align-items: center;
    flex-direction: column;
  }

  > div {
    @media ${Device.desktop} {
      width: 90%;
    }
  }
`;

export const Title = styled.p`
  margin: 0;
  padding: 0;
  font-family: 'Ubuntu';
  font-weight: bold;
  font-size: ${fontSize.big};
  text-align: left;
  color: ${color.text};

  @media ${Device.mobile}{
    font-size: 18px;
  }
`;

export const Text = styled.p`
  margin: 10px 0;
  padding: 0;
  font-family: 'Roboto';
  font-size: ${fontSize.small};
  text-align: left;
  line-height: 1rem;
  color: ${color.textLight};

  @media ${Device.mobile} {
    font-size: 12px;
  }

  a {
    color: ${color.red};
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
  font-size: ${fontSize.small};
  width: 100%;
`;

export const InputIconSection = styled.div`
  position: absolute;
  top: 0px;
  bottom: 0px;
  display: flex;
  align-items: center;
  right: 0px;
  padding: ${padding.tiny} 0;

  div{
    border-radius: 50%;
    background-color: ${color.red};
    height: 30px;
    width: 30px;
    margin-right: ${margin.tiny};
    display: flex;
    align-items: center;
    justify-content: center;

      img {
      height: 100%;
      max-height: 20px;
      max-width: 20px;
      cursor: pointer;
    }
  }
`;

export const SubmitButton = styled(SecondaryButton)`
  margin-left: 15px;

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
  margin-top: 30px;

  @media ${Device.mobile} {
    flex-direction: column;
  }
`;
