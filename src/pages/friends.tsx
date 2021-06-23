import React from 'react';
import { connect, useDispatch } from 'react-redux';

import { PageLayout } from '../layout/PageLayout';
import SEO from '../layout/SEO';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation } from '../state/app/app-actions';
import { DevelopmentPlaceholder } from '../layout/DevelopmentPlaceholder';

interface IFriendsPage {
  location: Location;
}

const FriendsPage = (props: IFriendsPage) => {
  const { location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    dispatch(LoadBrowserLocation(location));
  }, []);

  return (
    <PageLayout>
      <SEO title="Pola Web | Klub przyjaciół Poli" />
      <DevelopmentPlaceholder />
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({ location: state.app.location }), {})(FriendsPage);
