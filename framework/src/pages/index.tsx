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


const PageContainer = styled(PageSection)`

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

  console.log('render', users);
  return (
    <PageLayout>
      <SEO title="Pola Web" />
      <PageSection size="full">
          <Search />
      </PageSection>
      <PageContainer size="narrow">
        <Contents />
      </PageContainer>
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
