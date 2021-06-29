import React from 'react';
import { connect, useDispatch } from 'react-redux';

import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { DevelopmentPlaceholder } from '../layout/DevelopmentPlaceholder';
import { PageType } from '../domain/website';

interface ITeamPage {
  location?: Location;
}

const TeamPage = (props: ITeamPage) => {
  const { location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.TEAM));
    }
  }, []);

  return (
    <PageLayout>
      <SEOMetadata pageTitle="Dołącz do zespołu Pola" />
      <DevelopmentPlaceholder />
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({ location: state.app.location }), {})(TeamPage);
