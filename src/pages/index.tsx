import React from 'react';
import { connect } from 'react-redux';
import styled from 'styled-components';

import { PageLayout } from '../layout/PageLayout';
import SEO from '../layout/seo';
import { IState } from '../state/createStore';
import { ITodo } from '../models/todo';
import './index.css';
import Search from '../components/Search';
import Contents from '../components/Contents';
import { PageSection } from '../layout/PageSection';
import { Device, pageWidth, padding, theme } from '../styles/theme';

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

const MainPage = ({ todos = [], userId = 0 }: { todos: ITodo[] | undefined; userId: number | undefined }) => {
  const [amount, setAmount] = React.useState<number>(50);
  const [users, setUsers] = React.useState<IUser[]>([]);

  const load = () => {
    fetch(`https://randomuser.me/api/?results=${amount}`)
      .then(response => response.json())
      .then((response: IUsersResponse) => {
        console.log('users', response.results.length);
        setUsers(response.results);
      });
  };

  React.useEffect(() => {
    load();
  }, []);

  return (
    <PageLayout>
      <SEO title="Pola Web" />
      <PageSection size="full" backgroundColor={theme.dark}>
        <Content>
          <Search />
        </Content>
      </PageSection>
      <PageSection>
        <Contents />
      </PageSection>
    </PageLayout>
  );
};

const mapStateToProps = (state: IState) => {
  return {
    todos: state.todosReducer.todos,
    userId: state.loginReducer.userId,
  };
};

export default connect(mapStateToProps)(MainPage);
