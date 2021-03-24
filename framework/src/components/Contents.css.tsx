import styled from 'styled-components';

export const Wrapper = styled.div`
  display: flex;
  flex-wrap: wrap;

  @media only screen and (max-width: 1200px) {
    margin: 0 70px 20px 70px;
  }

  @media only screen and (max-width: 900px) {
    margin: 0 20px 20px 20px;
  }

  @media only screen and (max-width: 800px) {
    margin: 0 10px 20px 10px;
  }

  @media only screen and (max-width: 768px) {
    margin: 0;
  }
`;

export const Column = styled.div`
  flex: 0 50%;
`;

export const LeftColumn = styled.div`
  margin-right: 8px;
  height: 100%;
`;

export const RightColumn = styled.div`
  margin-left: 8px;
  height: 100%;
`;
