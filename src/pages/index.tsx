import React from 'react';
import { connect } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEO from '../layout/seo';
import { ITodo } from '../models/todo';
import './index.css';
import { SearchContainer } from '../components/search';
import Contents from '../components/Contents';
import { PageSection } from '../layout/PageSection';
import { Device, pageWidth, padding, theme } from '../styles/theme';
import { SearchService } from '../services/search-service';
import { IPolaState } from '../state/types';
import { searchDispatcher } from '../state/search/search-dispatcher';

const Content = styled.div`
  width: 100%;
  margin: 0 auto;
  @media ${Device.mobile} {
    padding: ${padding.normal};
  }
  @media ${Device.desktop} {
    padding: ${padding.normal} 0;
    max-width: ${pageWidth};
  }
`;

interface IMainPage {
  todos?: ITodo[];
  userId?: number;

  invokeSearch: (phrase: string) => void;
}

const MainPage = (props: IMainPage) => {
  const { todos = [], userId = 0 } = props;
  const [amount, setAmount] = React.useState<number>(50);
  const [users, setUsers] = React.useState<IUser[]>([]);

  const load = async () => {
    const products = await SearchService.getProducts(amount);

    console.log('users', products);
    setUsers(products);

    // fetch(`https://randomuser.me/api/?results=${amount}`)
    //   .then(response => response.json())
    //   .then((response: IUsersResponse) => {
    //     console.log('users', response.results.length);
    //     setUsers(response.results);
    //   });
  };

  React.useEffect(() => {
    load();
  }, []);

  return (
    <PageLayout>
      <SEO title="Pola Web" />
      <PageSection size="full" backgroundColor={theme.dark}>
        <Content>
          <SearchContainer searchResults={[]} onSearch={props.invokeSearch} />
        </Content>
      </PageSection>
      <PageSection>
        <Contents />
      </PageSection>
    </PageLayout>
  );
};

export default connect(
  (state: IPolaState) => ({
    //todos: state.todosReducer.todos,
    //userId: state.loginReducer.userId,
  }),
  {
    invokeSearch: searchDispatcher.invokePhrase,
  }
)(MainPage);
