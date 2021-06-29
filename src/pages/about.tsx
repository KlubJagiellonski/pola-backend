import React from 'react';
import { connect, useDispatch } from 'react-redux';

import { PageLayout } from '../layout/PageLayout';
import SEOMetadata from '../utils/browser/SEOMetadata';
import { IPolaState } from '../state/types';
import { LoadBrowserLocation, SelectActivePage } from '../state/app/app-actions';
import { DevelopmentPlaceholder } from '../layout/DevelopmentPlaceholder';
import About from '../components/About';
import { PageType } from '../domain/website';

interface IAboutPage {
  location?: Location;
}

const AboutPage = (props: IAboutPage) => {
  const { location } = props;
  const dispatch = useDispatch();

  React.useEffect(() => {
    if (location) {
      dispatch(LoadBrowserLocation(location));
      dispatch(SelectActivePage(PageType.ABOUT));
    }
  }, []);

  return (
    <PageLayout>
      <SEOMetadata pageTitle="O Poli" />
      <DevelopmentPlaceholder />
      <About />
    </PageLayout>
  );
};

export default connect((state: IPolaState) => ({ location: state.app.location }), {})(AboutPage);
