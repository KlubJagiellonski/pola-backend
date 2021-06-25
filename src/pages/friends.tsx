import React from 'react';
import { connect, useDispatch } from 'react-redux';

import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { DevelopmentPlaceholder } from '../layout/DevelopmentPlaceholder';
import { PageType } from '../domain/website';

interface IFriendsPage {
  location?: Location;
}

const FriendsPage = (props: IFriendsPage) => {
  const { location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.FRIENDS));
    }
  }, []);

  return (
    <PageLayout>
      <SEOMetadata title="Pola Web | Klub przyjaciół Poli" />
      <DevelopmentPlaceholder text="Treść przyjaciół Poli w budowie" />
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({ location: state.app.location }), {})(FriendsPage);
