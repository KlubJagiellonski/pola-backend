import styled from 'styled-components';
import {color, fontSize, Device} from './../styles/theme'
import {TitleSection} from './../styles/GlobalStyle.css'

export const Wrapper = styled.div`
  background: ${color.black};
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  min-height: 200px;
  padding: 35px 0;
  grid-area: download;

  @media ${Device.mobile}{
    min-height: 0;
  }
`;

export const DownoladTitle = styled(TitleSection)`
  color: ${color.white};
  margin: 30px 0 50px 0;
  font-size: ${fontSize.normal};

  @media ${Device.mobile}{
    margin-bottom: 30px;
  }
`

export const DownloadLinks = styled.div`
  a{
    padding: 10px;

    img{

      @media ${Device.mobile}{
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        width: 200px;
      }
    }
  }
`
